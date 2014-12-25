.. django-event-notification documentation master file, created by
   sphinx-quickstart on Tue Dec 16 11:38:19 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django_event's documentation!
===============================================

Django Event is notification system framework that allows you to push notifications to the browser.

Installing
~~~~~~~~~~

First you need pip. 
Use your OS's package system to install it.
On ubuntu you can install it like this: ::

    apt-get install python-pip
    
And it is highly recommended you to use python virtual environment. See `Virtualenv docs`_.

.. _`Virtualenv docs`: https://virtualenv.readthedocs.org/en/latest/

After that you need to install django-event: ::
    
    pip install git+https://github.com/ailove-dev/django-event
    
If you use Django Rest Framework and want to django-event provided REST api's for events use following command: ::

    pip install git+https://github.com/ailove-dev/django-event[rest_framework_api]


Contents:

.. toctree::
   django_event
   :maxdepth: 5

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

