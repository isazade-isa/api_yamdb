from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, ReviewsViewSet,
                    TitleViewSet, UserViewSet, CommentsViewSet,
                    ConfirmationCode, Token)


app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('users', UserViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentsViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path(r'auth/signup/', ConfirmationCode.as_view()),
    path(
        'auth/token/',
        Token.as_view(),
        name='token_obtain_pair'
    ),
]
