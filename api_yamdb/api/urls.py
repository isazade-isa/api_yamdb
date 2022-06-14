from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import UserViewSet, ProfileViewSet

router = SimpleRouter()

router.register(r'users', UserViewSet)
#router.register(r'users/me', ProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
