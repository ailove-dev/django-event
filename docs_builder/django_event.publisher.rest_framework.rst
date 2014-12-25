django_event.publisher.rest_framework
=====================================

django_event.publisher.serializers
----------------------------------

.. automodule:: django_event.publisher.rest_framework.serializers
    :members:
    :exclude-members: base_fields
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
