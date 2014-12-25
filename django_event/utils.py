# -*- coding: utf-8 -*-

"""
Utilities event module.
"""


import importlib


def import_var(var_path):
    """
    Imports variable.

    :param var_path: Module path in python representation.
    :type var_path: :class:`str`

    :return: Imported variable e.g. classes etc.
    :rtype: Anything you import.

    :raise: :class:`ImportError` if invalid module path passed into.
    """

    import_list = var_path.split('.')
    var_name = import_list.pop()
    var_package = '.'.join(import_list)
    try:
        var_module = importlib.import_module(var_package)
    except ImportError as e:
        e.message = 'Var %s not found' % import_list
        raise

    try:
        var = getattr(var_module, var_name)
    except AttributeError:
        raise ImportError('Var %s not found' % import_list)

    return var


def get_routing(user, routing_strategy):
    """
    Get routing key needed by event or listener.

    :param user: User to be routed.
    :type user: User

    :param routing_strategy: How it can compute routing key.
    :type routing_strategy: :class:`str`

    :return: Routing key for RabbitMQ
    :rtype: :class:`str`
    """

    routing = routing_strategy.split('.')
    source = user
    if routing[0] == 'user':
        routing = routing[1:]
    for route in routing:
        source = getattr(source, route)
    return str(source)