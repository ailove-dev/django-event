from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout


urlpatterns = patterns(
    '',
    url(
        r'',
        include('example.urls')
    ),
    url(
        regex=r'^login/$',
        view=login,
        kwargs={'template_name': 'login.html', 'redirect_field_name': 'next'},
        name='login'
    ),
    url(
        regex=r'^logout/$',
        view=logout,
        kwargs={'next_page': '/'},
        name='logout'
    ),
    url(
        r'',
        include('django_event.publisher.rest_framework.urls')
    )
)
