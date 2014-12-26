django_event.rabbitmq
=====================

django_event.rabbitmq.client
----------------------------

.. automodule:: django_event.rabbitmq.client
    :members:
    :exclude-members: RabbitMQClient
    :undoc-members:
    :show-inheritance:

.. autoclass:: RabbitMQClient(host=settings.RABBITMQ_HOST, port=settings.RABBITMQ_PORT, virtual_host=settings.RABBITMQ_VIRTUALHOST, username=settings.RABBITMQ_USERNAME, password=settings.RABBITMQ_PASSWORD, exchange_name='direct', exchange_type='direct')
    :members:
    :exclude-members: on_channel_open
    :show-inheritance:

    .. automethod:: on_channel_open(channel, callback=lambda frame: None)

