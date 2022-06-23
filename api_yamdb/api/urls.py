from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet, GenreViewSet, ReviewsViewSet, TitleViewSet, UserViewSet,
    CommentsViewSet, APIGetConfirmationCode, APIGetToken
)


app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', APIGetConfirmationCode.as_view()),
    path(
        'v1/auth/token/',
        APIGetToken.as_view(),
        name='token_obtain_pair'
    ),
]
