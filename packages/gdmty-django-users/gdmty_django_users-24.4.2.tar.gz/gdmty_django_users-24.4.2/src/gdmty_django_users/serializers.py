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

from rest_framework import serializers
from .models import User, Group
from django.contrib.auth.models import Permission

#


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['password', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'user_permissions', 'safe_delete',
                   'is_active']
        read_only_fields = ['last_login', 'username', 'date_joined', 'email', 'groups']


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'first_name', 'last_name']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
