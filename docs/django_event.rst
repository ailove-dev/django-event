django_event
============

.. toctree::

    django_event.management
    django_event.publisher
    django_event.rabbitmq
    django_event.subscriber

django_event.utils
------------------

.. automodule:: django_event.utils
    :members:
    :undoc-members:
    :show-inheritance:

django_event.settings
---------------------

.. automodule:: django_event.settings
    :members:
    :undoc-members:
    :show-inheritance:


django_event.publisher.models
-----------------------------

.. automodule:: django_event.models
    :members:
    :exclude-members: Event
    :undoc-members:
    :show-inheritance:

.. autoclass:: Event
    :members:
    :exclude-members: complete, send_message, start

    .. automethod:: complete(result, status=True, custom_message=None, callback=lambda event: None, errback=lambda event: None)
    .. automethod:: send_message(message, content_type, broadcast=False, callback=lambda event: None)
    .. automethod:: start(custom_message=None, callback=lambda event: None)


