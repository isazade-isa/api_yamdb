from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt import views as jwt_views

from .views import (CategoryViewSet, GenreViewSet,
                    TitleViewSet, UserViewSet,
                    ProfileViewSet, ConfirmationCode, Token)

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(r'users', UserViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
#router_v1.register(r'users/me', ProfileViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(r'auth/signup/', ConfirmationCode.as_view()),
    path(
        'auth/token/',
        Token.as_view(),
        name='token_obtain_pair'
    ),
]
