django_event.publisher
======================

.. toctree::
    
    django_event.publisher.rest_framework
    


django_event.publisher.decorator
--------------------------------

.. automodule:: django_event.publisher.decorator
    :members:
    :exclude-members: event
    :undoc-members:
    :show-inheritance:

.. autoclass:: event(event_type='', send_mail=False, progress_throttling=0.1, routing_strategy='', task_kwargs=None, on_start=lambda _event: None, on_success=lambda _event: None, on_error=lambda _event: None)
    :members:
    :show-inheritance:

    .. automethod:: __call__
    .. automethod:: __init__(event_type='', send_mail=False, progress_throttling=0.1, routing_strategy='', task_kwargs=None, on_start=lambda _event: None, on_success=lambda _event: None, on_error=lambda _event: None)

django_event.publisher.exceptions
---------------------------------

.. automodule:: django_event.publisher.exceptions
    :members:
    :undoc-members:
    :show-inheritance:

django_event.publisher.publisher
--------------------------------

.. automodule:: django_event.publisher.publisher
    :members:
    :exclude-members: BlockingPublisher, Publisher
    :undoc-members:
    :show-inheritance:

.. autoclass:: BlockingPublisher(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, virtual_host=settings.RABBITMQ_VIRTUALHOST, username=settings.RABBITMQ_USERNAME, password=settings.RABBITMQ_PASSWORD, exchange_name='direct', exchange_type='direct')
    :members:
    :show-inheritance:

.. autoclass:: Publisher(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, virtual_host=settings.RABBITMQ_VIRTUALHOST, username=settings.RABBITMQ_USERNAME, password=settings.RABBITMQ_PASSWORD, exchange_name='direct', exchange_type='direct')
    :members:
    :show-inheritance:

django_event.publisher.request
------------------------------

.. automodule:: django_event.publisher.request
    :members: _DummyRequest, _DummyUser
    :undoc-members:
    :exclude-members: EventRequest
    :show-inheritance:

.. autoclass:: EventRequest
    :members:
    :show-inheritance:
    
    .. automethod:: __getattr__
    
django_event.publisher.views
----------------------------

.. automodule:: django_event.publisher.views
    :members:
    :show-inheritance:
    :undoc-members:

django_event.publisher.urls
---------------------------

.. automodule:: django_event.publisher.rest_framework.urls
    :members:
    :undoc-members:
    :show-inheritance: