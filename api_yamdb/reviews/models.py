from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField()
    year = models.IntegerField()
    category_id =models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Review(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='title')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.SmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)


class Comment(models.Model):
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)

