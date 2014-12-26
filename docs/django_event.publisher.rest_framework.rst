django_event.publisher.rest_framework
=====================================

django_event.publisher.serializers
----------------------------------

.. automodule:: django_event.publisher.rest_framework.serializers
    :members:
    :exclude-members: EventSerializer, LocalDateTimeField
    :undoc-members:
    :show-inheritance:

.. autoclass:: EventSerializer(instance=None, data=None, files=None, context=None, partial=False, many=None, allow_add_remove=False, **kwargs)
    :members:
    :show-inheritance:
    
    .. class:: Meta
        
        .. attribute:: model
        
            alias of :class:`Event`
            
        .. attribute:: exclude
            :annotation: = ('event_request', 'task_name', 'task_id')
    
.. autoclass:: LocalDateTimeField(input_formats=None, format=None, *args, **kwargs)
    :members:
    :undoc-members:
    :show-inheritance:

django_event.publisher.urls
---------------------------

.. automodule:: django_event.publisher.rest_framework.urls
    :members:
    :undoc-members:
    :show-inheritance:

django_event.publisher.views
-----------------------------------

.. automodule:: django_event.publisher.rest_framework.views
    :members:
    :undoc-members:
    :exclude-members: post, get, EventListView
    :show-inheritance:

.. autoclass:: EventListView
    :members:
    :show-inheritance:
    :exclude-members: filter_backends

    .. attribute:: filter_backends
      :annotation: = (filters.OrderingFilter, )
      
      Filter backend. Provides basic ordering.
