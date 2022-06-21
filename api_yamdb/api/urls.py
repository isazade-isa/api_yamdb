from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, ReviewsViewSet,
                    TitleViewSet, UserViewSet, CommentsViewSet,
                    APIGetConfirmationCode, APIGetToken)


app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'users', UserViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewsViewSet, basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentsViewSet, basename='comments')


urlpatterns = [
    path('', include(router_v1.urls)),
<<<<<<< HEAD
    path('auth/signup/', ConfirmationCode.as_view()),
=======
    path('auth/signup/', APIGetConfirmationCode.as_view()),
>>>>>>> master
    path(
        'auth/token/',
        APIGetToken.as_view(),
        name='token_obtain_pair'
    ),
]
