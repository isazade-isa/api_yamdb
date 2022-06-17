from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from .views import UserViewSet, ConfirmationCode, Token

router = SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path(r'auth/signup/', ConfirmationCode.as_view()),
    path(
        'auth/token/',
        Token.as_view(),
        name='token_obtain_pair'
    ),
    path('', include(router.urls)),
]
