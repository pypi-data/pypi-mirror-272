#!-*- coding: utf-8 -*-
"""
Authentication backend for Django's Administration panel users based on email and password
This packages adds features such as group permissions and reCaptcha enterprise token verification.

This package is published as free software under the terms of the Apache License, Version 2.0. Is developed by
Dirección de Gobierno Digital of the Secretaría de Innovación y Gobierno Abierto of Municipality of Monterrey.

Authors: ['César Benjamín García Martínez <mathereall@gmail.com>', 'Miguel Angel Hernández Cortés
<miguelhdezc12@gmail.com>', 'César Guillermo Vázquez Álvarez <chechar.2001@gmail.com>']
Email: gobiernodigital@monterrey.gob.mx
GitHub: https://github.com/gobiernodigitalmonterrey/gdmty-drf-firebase-auth
Package: gdmty_django_users
PyPi: https://pypi.org/project/gdmty-django-users/
License: AGPL-3.0
"""

from django import forms
from django.utils.translation import gettext_lazy as _
from django.conf import settings

#


if 'wagtail.users' in settings.INSTALLED_APPS:
    from wagtail.users.forms import UserEditForm as WagtailUserEditForm, UserCreationForm as WagtailUserCreationForm

    class GdmtyWagtailUserEditForm(WagtailUserEditForm):
        username = forms.CharField(required=True, label=_("ID de usuario (username)"))


    class GdmtyWagtailUserCreationForm(WagtailUserCreationForm):
        username = forms.CharField(required=True, label=_("ID de usuario (username)"))
