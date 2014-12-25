# -*- coding: utf-8 -*-

"""
Synchronous views for django to get/cancel or retry events.
"""


from django.db.models import ObjectDoesNotExist
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EventSerializer
from ..models import Event


class EventListView(ListAPIView):
    """
    List all user events.
    """

    model = Event
    serializer_class = EventSerializer
    filter_backends = (OrderingFilter, )
    max_paginate_by = 50
    paginate_by = 10
    paginate_by_param = 'page_size'
    ordering = ('-completed_at', )
    permission_classes = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """
        Get user events
        ---

        """

        return super(EventListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(EventListView, self).get_queryset().filter(
            user=self.request.user)
        return qs

event_list = EventListView.as_view()


class EventDetailView(APIView):
    """
    Retrieve specific user event.
    """

    model = Event
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk):
        """
        Get event by id
        ---

        """

        try:
            event = Event.objects.get(pk=pk)
            if event.user == request.user:
                serializer = self.serializer_class(event)
                return Response(serializer.data)
            return Response(status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

event_detail = EventDetailView.as_view()


class CancelEventView(APIView):
    """
    Cancel executing event.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        """
        Cancel event by id
        ---

        omit_parameters:
            - form

        parameters:
            - name: pk
              required: true
              type: string
              paramType: path
        """

        try:
            event = Event.objects.get(pk=pk)
            if event.user == request.user and event.may_be_canceled:
                event.cancel()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

cancel_event = CancelEventView.as_view()


class RetryEventView(APIView):
    """
    Retry not completed event.
    """

    permission_classes = (IsAuthenticated, )

    def post(self, request, pk):
        """
        Cancel event by id
        ---

        omit_parameters:
            - form

        parameters:
            - name: pk
              required: true
              type: string
              paramType: path
        """

        try:
            event = Event.objects.get(id=pk)
            if event.user == request.user and event.may_be_retried:
                return Response({
                    'retried_id': event.retry()
                }, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_403_FORBIDDEN)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

retry_event = RetryEventView.as_view()