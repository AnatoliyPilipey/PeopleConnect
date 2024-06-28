from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import (
    Profile,
    Message,
)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "pseudonym",
            "first_name",
            "last_name",
            "description",
            "image",
        )


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "pseudonym",
            "first_name",
            "last_name",
            "description",
            "image",
        )

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)


class ProfileDetailSerializer(serializers.ModelSerializer):
    # subscribe = serializers.SerializerMethodField()
    # subscribe_me = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "pseudonym",
            "first_name",
            "last_name",
            "description",
            "subscribe",
            "subscribe_me",
            "image",
        )

    def get_subscribe_me(self, obj):
        subscribe_me = obj.subscribe_me.all()
        return ProfileDetailSerializer(subscribe_me, many=True).data


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "pseudonym",
            "first_name",
            "last_name",
            "description",
            "subscribe",
            "image"
        )


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="pseudonym",
    )
    class Meta:
        model = Message
        fields = (
            "id",
            "title",
            "author",
        )


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = (
            "title",
            "text",
            "image",
        )

    def create(self, validated_data):
        return Message.objects.create(
            author=Profile.objects.get(
                pk=self.context["request"].user.pk
            ),
            **validated_data,
        )


class MessageDetailSerializer(MessageSerializer):
    class Meta:
        model = Message
        fields = (
            "title",
            "author",
            "text",
            "image",
        )


class MessageUpdateSerializer(MessageSerializer):
    class Meta:
        model = Message
        fields = (
            "title",
            "text",
            "image",
        )
