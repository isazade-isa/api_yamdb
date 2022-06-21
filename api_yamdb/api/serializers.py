from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser

from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    rating = serializers.IntegerField(required=False)

    class Meta:
        model = Title
        fields = ('id', 'name', 'category', 'genre', 'year', 'description', 'rating')
        read_only_fields = ("id", "rating")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review', 'author')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title')
        model = Review

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        request = self.context['request']
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                    title=title,
                    author=request.user
            ).exists():
                raise ValidationError(
                    'Пользователь может добавить не '
                    'более одного ревью для каждого произведения.'
                )
        return data


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all()
            )
        ]
    )
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all()
            )
        ]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = CustomUser



class SingUpSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',)
        model = CustomUser


    @staticmethod
    def validate_username(value):
        if value == 'me':
            raise serializers.ValidationError(
                "Don't create user with username 'me'"
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)