from django_event.publisher import event

import time


@event(event_type='example_event_type', routing_strategy='user.id')
def test(event_request, event):
    for i in xrange(10):

        time.sleep(1)

        event.increment_progress(10)

    return 'example complete'
