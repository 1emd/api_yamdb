from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from reviews.validators import validate_year
from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50, db_index=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=50, db_index=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='titles',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True,
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=validate_year)
    description = models.TextField(
        max_length=200,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.CharField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            ),)

    def __str__(self):
        return self.text


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='comments'
    )
    text = models.TextField(max_length=200)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = pub_date = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text
