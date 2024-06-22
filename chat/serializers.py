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
            "pseudonym",
            "first_name",
            "last_name",
            "image",
        )
