import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify


def user_image_file_path(instance, filename):
    _, extension = os.path.split(filename)

    filename = f"{slugify(instance.first_name)}-{uuid.uuid4()}.{extension}"

    return os.path.join("upload/chat_user/", filename)


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    pseudonym = models.CharField(max_length=65, unique=True)
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    description = models.CharField(max_length=255, null=True)
    subscribe = models.ManyToManyField(
        "self",
        blank=True,
        symmetrical=False,
        related_name="subscribe_me",
    )
    image = models.ImageField(
        null=True,
        upload_to=user_image_file_path
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Message(models.Model):
    title = models.CharField(max_length=100, unique=True)
    text = models.CharField(max_length=255)
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    image = models.ImageField(
        null=True,
        upload_to=user_image_file_path
    )
