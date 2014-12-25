django_event.subscriber
=======================

django_event.subscriber.connection
----------------------------------

.. automodule:: django_event.subscriber.connection
    :members: _Request
    :undoc-members:
    :exclude-members: EventConnection
    :show-inheritance:

.. autoclass:: EventConnection(session)
    :members:
    :exclude-members: executor
    :undoc-members:
    :show-inheritance:

    .. attribute:: executor
	:annotation: = ThreadPoolExecutor(max_workers=cpu_count())

    	Thread pool for synchronous methods

django_event.subscriber.listeners
---------------------------------

.. automodule:: django_event.subscriber.listeners
    :members:
    :undoc-members:
    :show-inheritance:

django_event.subscriber.subscriber
----------------------------------

.. automodule:: django_event.subscriber.subscriber
    :members:
    :undoc-members:
    :show-inheritance:

