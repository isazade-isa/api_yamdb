from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters, mixins, viewsets, status

from users.models import CustomUser
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, UserSerializer,
    CommentSerializer, ReviewSerializer, TokenSerializer)
from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilterSet
from .permissions import IsAuthorOrStaffOrReadOnly


class CategoryViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAuthorOrStaffOrReadOnly)


class GenreViewSet(
        mixins.CreateModelMixin,
        mixins.ListModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    permission_classes = (IsAuthorOrStaffOrReadOnly)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilterSet
    permission_classes = (IsAuthorOrStaffOrReadOnly)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthorOrStaffOrReadOnly)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=True, permission_classes=[IsAuthenticated], methods=['get', 'patch'])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorOrStaffOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = self._get_title()
        return title.reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAuthorOrStaffOrReadOnly,
        IsAuthenticatedOrReadOnly
    )

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def perform_create(self, serializer):
        review = self._get_review()
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = self._get_review()
        return review.comments.all()


class ConfirmationCode(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = serializer.save()
        try:
            send_mail(
                'Confirmation code',
                'code: ' + default_token_generator.make_token(user=user),
                'yamdb.local',
                [user.email]
            )
        except BadHeaderError:
            Response(
                {'error': 'failed to send message.'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class Token(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(
            CustomUser, username=serializer.validated_data.get('username'))
        if default_token_generator.check_token(user, serializer.validated_data.get('confirmation_code')):
            token = RefreshToken.for_user(user)
            return Response(
                {'token': f'{token}'},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'incorrect'},
            status=status.HTTP_400_BAD_REQUEST
        )
