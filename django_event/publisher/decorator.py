# -*- coding: utf-8 -*-

"""
Core publisher client module.
Basically you should use this decorator instead of manually write events into
database.
Decorator specifies some overridable methods if you need basic customization.

Usage examples:

Defining event task: ::

    @event(event_type='some_type', routing_strategy='')
    def some_task(event_request, event):
        argument = event_request.custom_argument
        return some_processed_data(event_request.data, event)

And call: ::

    some_task.delay(EventRequest(django_request, custom_argument=123))

You can know more about .delay() or other methods in Celery docs.

"""


from __future__ import unicode_literals

from functools import wraps

from celery import task
from celery import current_task
from django.contrib.auth import get_user_model

from django_event.publisher.exceptions import EventError


class event(object):

    """
    Main client publisher interface.
    Decorates function and return celery task.

    Automatically start and end event after celery started/completed the
    task. You must pass EventRequest into decorated function.
    :class:`EventRequest` can accept keyword arguments needed by wrapped
    function which are not required but django request are required by internal
    needs. This decorator automatically set :class:`EventRequest` and
    :class:`Event` instances as wrapped function arguments.

    Wrapped func may raise specific exception :class:`EventError` used to notify
    subscribers about failure. Basically this decorator will handle only that
    type of exceptions. Be sure you handle all raised exception in wrapped func
    otherwise it will pass outside decorator and into database as well.
    """

    def __init__(self,
                 event_type='',
                 send_mail=False,
                 progress_throttling=0.1,
                 routing_strategy='',
                 task_kwargs=None,
                 on_start=lambda _event: None,
                 on_success=lambda _event: None,
                 on_error=lambda _event: None):

        """
        :param event_type: Event type, using in message routing.
        :type event_type: :class:`str`

        :param send_mail: Send email after event is done.
        :type send_mail: :class:`bool`

        :param progress_throttling: Describes how often event will send
         progress messages. See :class:`Event` docs for more information
         about this parameter.
        :type progress_throttling: :class:`float`

        :param routing_strategy: Routing strategy e.g. what listeners will do
         with messages. Empty strategy means you want to deliver notification to
         all subscribed clients. See :class:`Event` docs for more information
         about this parameter.
        :type routing_strategy: :class:`str`

        :param task_kwargs: Celery task arguments.
        :type task_kwargs: :class:`dict`

        :param on_start: Event start callback.
        :type on_start: :class:`str`

        :param on_success: Event success callback.
        :type on_success: callable object

        :param on_error: Event error callback.
        :type on_error: callable object
        """

        self._event_type = event_type
        self._send_mail = send_mail
        self._routing_strategy = routing_strategy
        self._progress_throttling = progress_throttling
        self._task_kwargs = task_kwargs or {}

        self._on_start = on_start
        self._on_success = on_success
        self._on_error = on_error

        self._user = None
        self._event_request = None
        self._event = None

        self._status = True
        self._result = None

    ############################################################################
    # CORE METHODS
    ############################################################################

    def create_event(self):
        """
        Create event model with passing arguments.
        Basically you dont need to manually create event.
        """

        from django_event.models import get_event_model

        event_model = get_event_model()

        self._event = event_model.create(
            progress_throttling=self._progress_throttling,
            routing_strategy=self._routing_strategy,
            user=self._user,
            type=self._event_type,
            send_mail=self._send_mail,
            task_id=current_task.request.id,
            task_name=current_task.name,
            event_request=self._event_request.serialize()
        )
        self._event.save()

    def __call__(self, func):
        """
        Wraps passed function into Celery :class:`Task`.

        :param func: Function to be wrapped.
        :type func: callable object

        :return: Celery task instance.
        :rtype: Celery :class:`Task`
        """

        @task(**self._task_kwargs)
        @wraps(func)
        def wrapped(event_request):
            self._event_request = event_request
            self._user = get_user_model().objects.get(
                id=self._event_request.user_id)
            self._send_mail = self._event_request.send_mail and self._send_mail

            self.create_event()
            self.start_event()
            try:
                self._result = func(self._event_request, self._event)
            except EventError as e:
                self._result = e.message
                self._status = False
            self.complete_event()

            return self._result

        return wrapped

    ############################################################################
    # OVERRIDABLE METHODS
    ############################################################################

    def start_event(self):
        """
        Starts event.
        Override this if you want to customize message.
        """

        self._event.start(callback=self._on_start)

    def complete_event(self):
        """
        Ends event.
        Override this if you want to customize message.
        """

        self._event.complete(
            self._result,
            status=self._status,
            callback=self._on_success,
            errback=self._on_error
        )