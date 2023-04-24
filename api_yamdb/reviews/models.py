from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .constants import MAX_REVIEW_SCORE_VALUE, MIN_REVIEW_SCORE_VALUE
from .validators import validate_year


class Category(models.Model):
    """Category model."""

    name = models.CharField(
        max_length=256,
        verbose_name='Category'
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        verbose_name='Slug of category'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Category'
        verbose_name_plural = 'Сategories'

    def __str__(self):
        """Return Category name."""
        return self.name


class CategoryImport(models.Model):
    """Category import model."""
    csv_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)


class Genre(models.Model):
    """Genre model."""

    name = models.CharField(
        max_length=256,
        verbose_name='Genre'
    )
    slug = models.SlugField(
        unique=True,
        db_index=True,
        blank=True,
        verbose_name='Slug of genre'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

    def __str__(self):
        """Return Genre name."""
        return self.name


class GenreImport(models.Model):
    """Genre import model."""
    csv_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)


class Title(models.Model):
    """Title model."""

    name = models.CharField(
        max_length=256,
        verbose_name='Title'
    )
    year = models.IntegerField(
        'year',
        validators=(validate_year, )
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description of title'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        related_query_name='query_titles',
        verbose_name='Genre',
        blank=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Category',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Title'
        verbose_name_plural = 'Titles'

    def __str__(self):
        """Return Title name."""
        return self.name


class TitleImport(models.Model):
    """Title import model."""
    csv_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    """Review model."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Date added',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveIntegerField(
        verbose_name='Score',
        validators=[MinValueValidator(MIN_REVIEW_SCORE_VALUE),
                    MaxValueValidator(MAX_REVIEW_SCORE_VALUE)]
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]

    def __str__(self):
        """Return review text."""
        return self.text


class ReviewImport(models.Model):
    """Review import model."""
    csv_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Comment model."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        verbose_name='Date added',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('id',)

    def __str__(self):
        """Return review comment text."""
        return self.text


class CommentImport(models.Model):
    """Comment model."""
    csv_file = models.FileField(upload_to='static/data/')
    date_added = models.DateTimeField(auto_now_add=True)
