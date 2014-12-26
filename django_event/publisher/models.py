# -*- coding: utf-8 -*-

"""
Core event model module.

You must handle old events by yourself using cron or celery worker.
"""


from datetime import timedelta

import celery
from django.conf import settings as app_settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .publisher import BlockingPublisher
from .request import EventRequest
from ..utils import get_routing
from .. import settings

class EventQuerySet(models.QuerySet):
    """
    Event query set and manager.
    Defines some useful shortcuts.
    """

    def not_viewed(self):
        """
        Not viewed events.

        :return: Not viewed events.
        :rtype: :class:`EventQuerySet`
        """

        return self.filter(viewed=False)

    def viewed(self):
        """
        Viewed events.

        :return: Viewed events.
        :rtype: :class:`EventQuerySet`
        """

        return self.filter(viewed=True)

    def old(self):
        """
        Old events.

        :return: Old events.
        :rtype: :class:`EventQuerySet`
        """

        storing_days = settings.STORE_DAY
        return self.filter(
            completed_at__lte=timezone.now() - timedelta(days=storing_days)
        )

    def completed(self):
        """
        Completed events.

        :return: Completed events.
        :rtype: :class:`EventQuerySet`
        """

        return self.filter(completed=True)

    def not_completed(self):
        """
        Not completed events.

        :return: Not completed events.
        :rtype: :class:`EventQuerySet`
        """

        return self.filter(completed=False)

    def successful(self):
        """
        Successful events.

        :return: Successful events.
        :rtype: :class:`EventQuerySet`
        """

        return self.filter(completed=True, status=True)

    def failed(self):
        """
        Failed events.

        :return: Failed events.
        :rtype: :class:`EventQuerySet`
        """

        return self.filter(completed=True, status=False)

    def mark_viewed(self):
        """
        Mark completed events as viewed.
        """

        self.completed().not_viewed().update(viewed=True)


class Event(models.Model):
    """
    Core event class.
    Don't inherit this model.
    Majority of model methods have custom_message parameter in case if you
    don't like/need default message protocol.
    Most of the methods are for private need i.e. all on_* methods. Be sure
    to not use these methods directly.
    """

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    objects = EventQuerySet.as_manager()

    user = models.ForeignKey(getattr(app_settings, 'AUTH_USER_MODEL', User))
    type = models.CharField(max_length=30)
    send_mail = models.BooleanField(default=False)

    task_id = models.CharField(max_length=256, null=True)
    task_name = models.CharField(max_length=256, editable=False)
    event_request = models.TextField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    canceled = models.BooleanField(default=False)
    retried = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    status = models.BooleanField(default=True)
    result = models.TextField(null=True)

    def __init__(self, *args, **kwargs):
        """
        Init model method. You don't basically need to call this method
        manually. Instead use .create() method.

        :param args: Model args.
        :param kwargs: Model kwargs.
        """

        super(Event, self).__init__(*args, **kwargs)

        self._publisher = BlockingPublisher()
        self._progress = 0.0
        self._retried_id = None
        self._progress_throttling = None
        self._routing_strategy = None
        self._routing_key = None

    @classmethod
    def create(cls,
               progress_throttling=0.1,
               routing_strategy='',
               *args, **kwargs):
        """
        Fabric method for event creature. Use this as main event creature
        source.

        :param progress_throttling: Describes how often event will send
         progress messages when user increments progress via
         :func:`increment_progress` method. :class:`Event` will not send
         any progress messages with out user actions on
         :func:`increment_progress`. If you don't need progress you may not
         specify this parameter and not use :func:`increment_progress` method.
        :type progress_throttling: :class:`float`

        :param routing_strategy: Routing strategy e.g. what listeners will do
         with messages. Empty strategy means you want to deliver notification to
         all subscribed clients.
        :type routing_strategy: :class:`str`

        :param args: Model init args

        :param kwargs: Model init kwargs

        :return: Created and configured event.
        :rtype: :class:`Event`
        """

        event = cls(*args, **kwargs)
        event._progress_throttling = progress_throttling
        event._routing_strategy = routing_strategy
        event._routing_key = get_routing(event.user, routing_strategy)
        return event

    ############################################################################
    # SHORTCUTS
    ############################################################################

    @property
    def failure(self):
        """
        Shortcut for event status.

        :return: True if event failed else False.
        :rtype: :class:`bool`
        """

        return True if not self.status else False

    @property
    def success(self):
        """
        Shortcut for event status.

        :return: True if event succeed else False.
        :rtype: :class:`bool`
        """

        return not self.failure

    @property
    def may_be_retried(self):
        """
        Shortcut for event state.

        :return: Check if event may be retried.
        :rtype: :class:`bool`
        """

        return (self.canceled or self.failure) and not self.retried

    @property
    def may_be_canceled(self):
        """
        Shortcut for event state.

        :return: Check if event may be canceled.
        :rtype: :class:`bool`
        """

        return (
            self.started
            and not self.completed and not self.canceled and not self.retried
        )

    @classmethod
    def delete_old(cls):
        """
        Deletes old events.
        """

        cls.objects.viewed().old().delete()

    def view(self):
        """
        Mark instance as viewed.
        """

        self.viewed = True
        self.save()

    ############################################################################
    # EXECUTING METHODS
    ############################################################################

    def start(self,
              custom_message=None,
              callback=lambda event: None):
        """
        Start event and save state into database. It will always call passed
        callback.

        :param custom_message: Overrides default message.
        :type custom_message: JSON serializable object.

        :param callback: Callback after event started
        :type callback: callable object
        """

        self.started = True
        self.started_at = timezone.now()
        self.save()

        self._publisher.connect()
        self.on_start(custom_message)
        callback(self)

    def complete(self,
                 result,
                 status=True,
                 custom_message=None,
                 callback=lambda event: None,
                 errback=lambda event: None):
        """
        Complete event and save state into database. It will always call passed
        callback.

        :param result: Task result.
        :type result: JSON serializable object.

        :param status: Describes task result status e.g. task raised exception
         will set False status.

        :type status: :class:`bool`

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.

        :param callback: Callback after event ended with success.
        :type callback: callable object

        :param errback: Callback after event ended with error.
        :type errback: callable object
        """

        self.completed = True
        self.status = status
        self.result = result
        self.completed_at = timezone.now()
        self.save()

        self.on_complete(custom_message, callback, errback)
        self._publisher.disconnect()

    def increment_progress(self, progress_delta, custom_message=None):
        """
        Increments event progress with out saving to database.
        If custom message passed it will send it instead of default message.

        :param progress_delta: Progress delta.
        :type progress_delta: :class:`float`

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        if self._progress + progress_delta > 100.0:
            self._progress = 99.9
        else:
            self._progress += progress_delta
        if progress_delta >= self._progress_throttling:
            self.on_progress_change(custom_message)

    def retry(self, custom_message=None, request=None, **kwargs):
        """
        Retry not completed event.
        If custom message passed it will send it instead of default message.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        if not request or not kwargs:
            retry_request = EventRequest.deserialize(self.event_request)
        else:
            retry_request = EventRequest(request, **kwargs)
        new_task_id = celery.current_app.send_task(
            self.task_name,
            args=(retry_request, )
        ).id
        self.retried = True
        self.viewed = True
        self.save()
        self.on_retry(custom_message)

        self._retried_id = Event.objects.get(task_id=new_task_id).id
        return self._retried_id

    def cancel(self, custom_message=None):
        """
        Cancel executing event.
        If custom message passed it will send it instead of default message.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        celery.task.control.revoke(self.task_id, terminate=True)
        self.canceled = True
        self.viewed = True
        self.save()
        self.on_cancel(custom_message)

    ############################################################################
    # CALLBACKS
    ############################################################################

    def on_start(self, custom_message):
        """
        Start callback. Sends message to subscribed clients.
        If custom message passed it will send it instead of default message.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        if custom_message:
            self._publisher.publish_message(
                custom_message
            )
            return
        self._publisher.publish_message({
            'message': {
                self.id: {
                    'type': self.type,
                    'action': 'started',
                    'status': None,
                    'body': None,
                    'error': None
                }
            },
            'routing_strategy': self._routing_strategy,
            'routing_key': self._routing_key
        }, routing_key=self.type)

    def on_complete(self, custom_message, callback, errback):
        """
        Complete callback. Dispatch between success and error status.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.

        :param callback: Callback after event ended with success.
        :type callback: callable object

        :param errback: Callback after event ended with error.
        :type errback: callable object
        """

        if self.status:
            self.on_success(custom_message, callback)
        else:
            self.on_error(custom_message, errback)

    def on_success(self, custom_message, callback):
        """
        Success callback. Sends message to subscribed clients.

        :param custom_message: Custom message
        :type custom_message: JSON serializable object.

        :param callback: Callback after event ended with success.
        :type callback: callable object
        """

        if custom_message:
            self._publisher.publish_message(
                custom_message
            )
            return
        self._publisher.publish_message({
            'message': {
                self.id: {
                    'type': self.type,
                    'action': 'completed',
                    'status': 'success',
                    'body': self.result,
                    'error': None
                }
            },
            'routing_strategy': self._routing_strategy,
            'routing_key': self._routing_key
        }, routing_key=self.type)
        callback(self)

    def on_error(self, custom_message, errback):
        """
        Error callback. Sends message to subscribed clients.

        :param custom_message: Custom message
        :type custom_message: JSON serializable object.

        :param errback: Errback after event ended with error.
        :type errback: callable object
        """

        if custom_message:
            self._publisher.publish_message(
                custom_message
            )
            return
        self._publisher.publish_message({
            'message': {
                self.id: {
                    'type': self.type,
                    'action': 'completed',
                    'status': 'error',
                    'body': None,
                    'error': self.result
                }
            },
            'routing_strategy': self._routing_strategy,
            'routing_key': self._routing_key
        }, routing_key=self.type)
        errback(self)

    def on_progress_change(self, custom_message):
        """
        Progress change callback. Sends message to subscribed clients.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        if custom_message:
            self._publisher.publish_message(
                custom_message
            )
            return
        self._publisher.publish_message({
            'message': {
                self.id: {
                    'type': self.type,
                    'action': 'progress_change',
                    'status': self._progress,
                    'body': None,
                    'error': None
                }
            },
            'routing_strategy': self._routing_strategy,
            'routing_key': self._routing_key
        }, routing_key=self.type)

    def on_cancel(self, custom_message):
        """
        Cancel callback. Sends message to subscribed clients.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        if custom_message:
            self._publisher.publish_message(
                custom_message
            )
            return
        self._publisher.publish_message({
            'message': {
                self.id: {
                    'type': self.type,
                    'action': 'canceled',
                    'status': None,
                    'body': None,
                    'error': None
                }
            },
            'routing_strategy': self._routing_strategy,
            'routing_key': self._routing_key
        }, routing_key=self.type)

    def on_retry(self, custom_message):
        """
        Cancel callback. Sends message to subscribed clients.

        :param custom_message: Custom message.
        :type custom_message: JSON serializable object.
        """

        if custom_message:
            self._publisher.publish_message(
                custom_message
            )
            return
        self._publisher.publish_message({
            'message': {
                self.id: {
                    'type': self.type,
                    'action': 'retried',
                    'status': None,
                    'body': self._retried_id,
                    'error': None
                }
            },
            'routing_strategy': self._routing_strategy,
            'routing_key': self._routing_key
        }, routing_key=self.type)

    ############################################################################
    # SEND METHODS
    ############################################################################

    def send_message(self,
                     message,
                     content_type,
                     broadcast=False,
                     callback=lambda event: None):
        """
        Send custom message to subscribed clients and execute passed callback.

        :param message: Message.
        :type message: :class:`str`

        :param content_type: Message content type.
        :type content_type: :class:`str`

        :param broadcast: True if you need broadcast.
        :type broadcast: :class:`bool`

        :param callback: Callback after message send.
        :type callback: callable object
        """

        self._publisher.publish_message(
            message,
            content_type=content_type,
            routing_key='' if broadcast else str(self.user.id)
        )
        callback(self)

    def send_email(self):
        """
        Sends email to user after event is done.

        TODO: implement email sending.
        """

        # TODO: Implement email sending
        pass