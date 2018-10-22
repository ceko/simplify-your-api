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
class TranslationHistory(models.Model):
    created_on = models.DateTimeField(auto_now=True)
    request = models.CharField(max_length=255)
    response = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )

# Serializers go here

class TranslationSerializer(ModelSerializer):
    response = CharField(read_only=True)

    def create(self, validated_data):
        return TranslationHistory.objects.create(
            **validated_data,
            user=self.context['request'].user,
            response=to_yodish(validated_data.get('request'))
        )

    class Meta:
        model = TranslationHistory
        fields = ('request','response','created_on','id')

# Viewsets/Endpoints go here

@api_view(['GET'])
def version(request):
    return Response({
        'version': {
            'major': 0,
            'minor': 0,
            'patch': 1
        }
    })

urlpatterns += [
    path(r'version/', version),
]

class DefaultThrottle(UserRateThrottle):
    rate = '5/sec'

class DefaultPagination(CursorPagination):
    page_size = 5
    ordering = '-created_on'

class TranslationViewSet(viewsets.ModelViewSet):
    serializer_class = TranslationSerializer
    queryset = TranslationHistory.objects.all().order_by(
        '-created_on'
    )
    authentication_classes = [
        TokenAuthentication,
        SessionAuthentication
    ]
    permission_classes = [
        IsAuthenticated
    ]
    throttle_classes = [DefaultThrottle,]
    http_method_names = ['get', 'post']
    pagination_class = DefaultPagination

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

api_router = routers.DefaultRouter()
api_router.register(r'translations', TranslationViewSet)

urlpatterns += api_router.urls