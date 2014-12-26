# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from django_event.models import Event


class LoginRequiredMixin(object):
    """
    Event view mixin class with overrided :func:`dispatch` method to restrict
    anonymous users.
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to implement auth restriction.

        :param request: Incoming request.
        :type request: :class:`HttpRequest`

        :return: Response.
        :rtype: :class:`HttpResponse`
        """

        return super(LoginRequiredMixin, self).dispatch(
            request, *args, **kwargs
        )


class EventListMixin(object):
    """
    Event view mixin class with overrided :func:`get_queryset` method.
    """

    model = Event

    def get_queryset(self):
        """
        Returns user-owned events.

        :return: QuerySet of user-owned events.
        :rtype: :class:`EventQuerySet`
        """

        return get_list_or_404(self.model, user=self.request.user)


class EventListBaseView(LoginRequiredMixin,
                        EventListMixin, ListView):
    """
    Base event list view class.
    """

class EventDetailMixin(EventListMixin):
    """
    Event view mixin class with overrided :func:`get_object` method.
    """

    def get_object(self, pk, queryset=None):
        """
        Returns user-owned event by id.

        :return: QuerySet of user-owned events.
        :rtype: :class:`Event`
        """

        return get_object_or_404(self.get_queryset(), pk=pk)


class EventDetailBaseView(LoginRequiredMixin,
                          EventDetailMixin, DetailView):
    """
    Base event detail view class.
    """


class CancelEventBaseView(LoginRequiredMixin,
                          EventDetailMixin, View):
    """
    Base cancel event view class.
    """

    def cancel(self, pk):
        """
        Returns True if event is successfully canceled False otherwise.

        :param pk: Event id.
        :type pk: :class:`int`

        :return: True if canceled else False.
        :rtype: :class:`bool`
        """

        event = self.get_object(pk)
        if event.may_be_canceled:
            event.cancel()
            return True
        return False

    def post(self, request, pk):
        return HttpResponse(self.cancel(pk))


class RetryEventBaseView(LoginRequiredMixin,
                         EventDetailMixin, View):
    """
    Base retry event view class.
    """

    def retry(self, pk):
        """

        Returns new event id if it successfully retried event None otherwise.

        :param pk: Event id.
        :type pk: :class:`int`

        :return: New event id if retried else None.
        :rtype: :class:`int` or None
        """

        event = self.get_object(pk)
        return event.retry() if event.may_be_retried else None

    def post(self, request, pk):
        return HttpResponse(self.retry(pk))