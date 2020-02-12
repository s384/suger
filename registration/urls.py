from django.urls import path
from django.conf.urls import url
from .views import (account_activation_sent, activate, ActivationForm,
                FirstLogin)


urlpatterns = [
    url(r'^activacion-cuenta/$', ActivationForm.as_view(), name='account_activation_form'),
    url(r'^activacion-cuenta-enviado/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activacion/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='activate'),
    url('primer_inicio/', FirstLogin.as_view(), name='first_login'),
]