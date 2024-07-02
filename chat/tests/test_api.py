from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.db.models import Value, IntegerField
from rest_framework.test import APIClient
from rest_framework import status
from chat.models import (
    Profile,
    Message,
)
from chat.serializers import (
    ProfileDetailSerializer,
    ProfileSerializer,
    MessageDetailSerializer,
    MessageSerializer,
)


MESSAGE_URL = reverse("chat:message-list")
PROFILE_URL = reverse("chat:profile-list")


def detail_message_url(detail_id: int):
    return reverse("chat:message-detail", args=[detail_id])


def detail_profile_url(detail_id: int):
    return reverse("chat:profile-detail", args=[detail_id])


def sample_profile(new_user, pseudonym, **params):
    defaults = {
        "user": new_user,
        "pseudonym": pseudonym,
        "first_name": "Anatoliy",
        "last_name": "Perviy",
        "description": "My profile",
    }
    defaults.update(params)
    return Profile.objects.create(**defaults)

class UnauthenticatedMessageApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_un_auth_required_list(self):
        res = self.client.get(MESSAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_un_auth_required_detail(self):
        res = self.client.get(detail_message_url(1))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class UnauthenticatedProfileApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_un_auth_required_list(self):
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_un_auth_required_detail(self):
        res = self.client.get(detail_profile_url(1))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedProfileApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_profile_detail(self):
        profile = sample_profile(self.user, "author")
        res = self.client.get(detail_profile_url(self.user.pk))

        serializer = ProfileDetailSerializer(profile, many=False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_profile_list(self):
        sample_profile(self.user, "author")

        user_new = get_user_model().objects.create_user(
            "testnew@test.com",
            "testnewpassword"
        )
        sample_profile(user_new, "Cheh")

        res = self.client.get(PROFILE_URL)
        profile = Profile.objects.all()
        serializer = ProfileSerializer(profile, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_profile_list(self):
        sample_profile(self.user, "author")

        user_new = get_user_model().objects.create_user(
            "testnew@test.com",
            "testnewpassword"
        )
        sample_profile(
            user_new,
            "Cheh",
            first_name="Nikolay",
            description="New description"
        )
        res1 = self.client.get(
            PROFILE_URL,
            {"pseudonym": "Cheh"}
        )
        res2 = self.client.get(
            PROFILE_URL,
            {"name": "niko"}
        )
        res3 = self.client.get(
            PROFILE_URL,
            {"description": "new"}
        )

        profile = Profile.objects.get(pk=2)
        serializer = ProfileSerializer(profile, many=False)
        self.assertEqual(res1.status_code, status.HTTP_200_OK)

        self.assertEqual(res1.data[0], serializer.data)
        self.assertEqual(res2.data[0], serializer.data)
        self.assertEqual(res3.data[0], serializer.data)


class AuthenticatedMessageApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_auth_required_detail(self):
        message = Message.objects.create(
            title="Chill",
            text="Sample text",
            author=sample_profile(self.user, "author")

        )

        res = self.client.get(detail_message_url(self.user.pk))
        serializer = MessageDetailSerializer(message, many=False)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_auth_required_list(self):
        profile = sample_profile(self.user, "author")
        Message.objects.create(
            title="Chill",
            text="Sample text",
            author=profile

        )
        Message.objects.create(
            title="Chill new",
            text="Sample text",
            author=profile

        )

        res = self.client.get(MESSAGE_URL)
        message = Message.objects.all()
        serializer = MessageSerializer(message, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
