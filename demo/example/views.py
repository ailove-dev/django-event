from django.shortcuts import render_to_response
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

from .tasks import test
from django_event.publisher.request import EventRequest


@login_required
def example(request):
    return render_to_response('example.html')


@login_required
def example_start(request):
    test.delay(EventRequest(request))
    return HttpResponse(status=200)
