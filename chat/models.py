import os
import uuid
from django.db import models
from django.utils.text import slugify


def user_image_file_path(instance, filename):
    _, extension = os.path.split(filename)

    filename = f"{slugify(instance.first_name)}-{uuid.uuid4()}.{extension}"

    return os.path.join("upload/crew/", filename)


class Profile(models.Model):
    pseudonym = models.CharField(max_length=65, unique=True)
    first_name = models.CharField(max_length=65)
    last_name = models.CharField(max_length=65)
    image = models.ImageField(
        null=True,
        upload_to=user_image_file_path
    )

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Subscribe(models.Model):
    pseudonym_id = models.IntegerField()
    my_subscribe = models.ManyToManyField(
        Profile,
        related_name="subscribe"
    )
