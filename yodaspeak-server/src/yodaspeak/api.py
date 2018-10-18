"""
This single file is where we'll do all of our API work.
"""

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.urls import path
from rest_framework import permissions, routers, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.decorators import api_view
from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField, ModelSerializer, Serializer
from rest_framework.throttling import UserRateThrottle
from translator import to_yodish

urlpatterns = []

# Models go here

# Serializers go here

# Viewsets/Endpoints go here