from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Count
from chat.permissions import IsAdminOrIfAuthenticatedReadOnly
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.db.models import Q
from chat.models import (
    Profile,
    Message,
)
from chat.serializers import (
    ProfileSerializer,
    ProfileCreateSerializer,
    ProfileDetailSerializer,
    ProfileUpdateSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    MessageDetailSerializer,
    MessageUpdateSerializer,
)


class ProfileViewSet(viewsets.ModelViewSet):
    """Profile"""
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            pseudonym = self.request.query_params.get("pseudonym")
            description = self.request.query_params.get("description")
            name = self.request.query_params.get("name")
            if pseudonym:
                queryset = queryset.filter(pseudonym__icontains=pseudonym)
            if description:
                queryset = queryset.filter(description__icontains=description)
            if name:
                queryset = queryset.filter(
                    Q(first_name__icontains=name) |
                    Q(last_name__icontains=name)
                )

        return queryset

    def get_serializer_class(self):
        if self.action == "create":
            return ProfileCreateSerializer
        if self.action == "retrieve":
            return ProfileDetailSerializer
        if self.action == "update":
            return ProfileUpdateSerializer
        return ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "pseudonym",
                type={"type": "str"},
                description="Filter by pseudonym User"
                            "(ex. ?pseudonym=Ki"
            ),
            OpenApiParameter(
                "description",
                type={"type": "str"},
                description="Filter by description User"
                            "(ex. ?description=Ki"
            ),
            OpenApiParameter(
                "name",
                type={"type": "str"},
                description="Filter by first_name & last_name "
                            "(ex. ?name=Ki"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        """Profile have more information about User"""
        return super().list(request, *args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_permissions(self):
        if self.action != "list":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get_serializer_class(self):
        serializer = self.serializer_class
        if self.action == "create":
            serializer = MessageCreateSerializer
        if self.action == "retrieve":
            serializer = MessageDetailSerializer
        if self.action == "update":
            serializer = MessageUpdateSerializer
        return serializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            pseudonym = self.request.query_params.get("pseudonym")
            text = self.request.query_params.get("text")
            if pseudonym:
                queryset = queryset.filter(author__pseudonym__icontains=pseudonym)
            if text:
                queryset = queryset.filter(
                    Q(title__icontains=text) |
                    Q(text__icontains=text)
                )
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "pseudonym",
                type={"type": "str"},
                description="Filter by pseudonym User"
                            "(ex. ?pseudonym=Ki"
            ),
            OpenApiParameter(
                "text",
                type={"type": "str"},
                description="Filter by title & text"
                            "(ex. ?description=Ki"
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """Message from Profile(User)"""
        return super().list(request, *args, **kwargs)
