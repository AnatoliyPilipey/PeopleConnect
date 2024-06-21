from django.urls import path, include
from rest_framework import routers
from chat.views import (
    ProfileViewSet,
    SubscribeViewSet,
)


router = routers.DefaultRouter()
router.register("profile", ProfileViewSet)
router.register("subscribe", SubscribeViewSet)


urlpatterns = [path("", include(router.urls))]


app_name = "chat"
