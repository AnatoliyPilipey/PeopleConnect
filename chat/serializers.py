from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import (
    Profile,
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
            # "subscribe",
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
