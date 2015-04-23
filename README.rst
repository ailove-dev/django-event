README
======


About
-----

Django Event is notification system framework that allows you to push notifications to the browser.

Installing
~~~~~~~~~~

First you need pip. 
Use your OS's package system to install it.
On ubuntu you can install it like this:

    apt-get install python-pip
    
And it is highly recommended you to use python virtual environment. See `Virtualenv docs`_.

.. _`Virtualenv docs`: https://virtualenv.readthedocs.org/en/latest/

After that you need to install ailove-django-event:
    
    pip install git+https://github.com/ailove-dev/django-event
    
If you use Django Rest Framework and want to django-event provided REST api's for events ensure you installed
Django Rest Framework 3.1.1 or newer.

    pip install djangorestframework>=3.1.1
    

Documentation
~~~~~~~~~~~~~

For docs we use Read The Docs and you can find our docs `here`_.
    
.. _`here`: https://django-event.readthedocs.org/
    