from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес категории'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Навзвание произведения'
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        db_index=True,
        blank=True,
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name

      
class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Адрес жанра'
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

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
