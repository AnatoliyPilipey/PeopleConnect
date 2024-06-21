from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Count
from chat.permissions import IsAdminOrIfAuthenticatedReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter
from chat.models import (
    Profile,
    Subscribe,
)
from chat.serializers import (
    ProfileSerializer,
    SubscribeSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    """Profile"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)


class SubscribeViewSet(viewsets.ModelViewSet):
    """Subscribe"""
    queryset = Subscribe.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = (IsAdminOrIfAuthenticatedReadOnly,)
