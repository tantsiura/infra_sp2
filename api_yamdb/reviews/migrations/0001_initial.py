# Generated by Django 3.2 on 2023-03-30 12:29

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Category')),
                ('slug', models.SlugField(unique=True, verbose_name='Slug of category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Сategories',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CategoryImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='static/data/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date added')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='CommentImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='static/data/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Genre')),
                ('slug', models.SlugField(blank=True, unique=True, verbose_name='Slug of genre')),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='GenreImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='static/data/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Date added')),
                ('score', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Score')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='ReviewImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='static/data/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TitleImport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('csv_file', models.FileField(upload_to='static/data/')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Title')),
                ('year', models.IntegerField(validators=[reviews.validators.validate_year], verbose_name='year')),
                ('description', models.TextField(blank=True, verbose_name='Description of title')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category', verbose_name='Category')),
                ('genre', models.ManyToManyField(blank=True, related_name='titles', related_query_name='query_titles', to='reviews.Genre', verbose_name='Genre')),
            ],
            options={
                'verbose_name': 'Title',
                'verbose_name_plural': 'Titles',
                'ordering': ('id',),
            },
        ),
    ]
