import csv

from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse

from .forms import (CategoryImportForm, CommentImportForm, GenreImportForm,
                    ReviewImportForm, TitleImportForm)
from .models import (Category, CategoryImport, Comment, CommentImport, Genre,
                     GenreImport, Review, ReviewImport, Title, TitleImport)


@admin.register(CategoryImport)
class CategoryImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


admin.site.register(Category)


class CategoryAdmin(admin.ModelAdmin):
    """Model for adding data by category."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-empty-'

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = CategoryImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'name', 'slug']:
                        messages.warning(request, 'Invalid file headers')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        Category.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
                url = reverse('admin:index')
                messages.success(request, 'File imported successfully')
                return HttpResponseRedirect(url)
        form = CategoryImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(GenreImport)
class GenreImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


admin.site.register(Genre)


class GenreAdmin(admin.ModelAdmin):
    """Model for adding data by genre."""
    list_display = (
        'name',
        'slug',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = 'empty'

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = GenreImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'name', 'slug']:
                        messages.warning(request, 'Invalid file headers')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        Genre.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            slug=row[2]
                        )
                url = reverse('admin:index')
                messages.success(request, 'File imported successfully')
                return HttpResponseRedirect(url)
        form = GenreImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(TitleImport)
class TitleImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


admin.site.register(Title)


class TitleAdmin(admin.ModelAdmin):
    """Model for adding data by title."""
    list_display = (
        'name',
        'year',
        'category',
        'description',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = 'empty'

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = TitleImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'name', 'year', 'description',
                                      'category_id']:
                        messages.warning(request, 'Invalid file headers')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        Title.objects.update_or_create(
                            id=row[0],
                            name=row[1],
                            year=row[2],
                            description=row[3],
                            category_id=row[4]
                        )
                url = reverse('admin:index')
                messages.success(request, 'File imported successfully')
                return HttpResponseRedirect(url)
        form = TitleImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(ReviewImport)
class ReviewImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


admin.site.register(Review)


class ReviewAdmin(admin.ModelAdmin):
    """Model for adding data by review."""
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = 'empty'

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = ReviewImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'text', 'pub_date', 'score',
                                      'author_id', 'title_id']:
                        messages.warning(request, 'Invalid file headers')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        Review.objects.update_or_create(
                            name=row[0],
                            text=row[1],
                            pub_date=row[2],
                            score=row[3],
                            author_id=row[4],
                            title_id=row[5]
                        )
                url = reverse('admin:index')
                messages.success(request, 'File imported successfully')
                return HttpResponseRedirect(url)
        form = ReviewImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})


@admin.register(CommentImport)
class CommentImportAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'date_added')


admin.site.register(Comment)


class CommentAdmin(admin.ModelAdmin):
    """Model for adding data by comment."""
    list_display = (
        'review',
        'text',
        'author',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = 'empty'

    def get_urls(self):
        urls = super().get_urls()
        urls.insert(-1, path('csv-upload/', self.upload_csv))
        return urls

    def upload_csv(self, request):
        if request.method == 'POST':
            form = CommentImportForm(request.POST, request.FILES)
            if form.is_valid():
                form_object = form.save()
                with form_object.csv_file.open('r') as csv_file:
                    rows = csv.reader(csv_file, delimiter=',')
                    if next(rows) != ['id', 'text', 'pub_date',
                                      'author_id', 'review_id']:
                        messages.warning(request, 'Invalid file headers')
                        return HttpResponseRedirect(request.path_info)
                    for row in rows:
                        print(row[2])
                        Category.objects.update_or_create(
                            id=row[0],
                            text=row[1],
                            pub_date=row[3],
                            author_id=row[4],
                            review_id=row[5]
                        )
                url = reverse('admin:index')
                messages.success(request, 'File imported successfully')
                return HttpResponseRedirect(url)
        form = CommentImportForm()
        return render(request, 'admin/csv_import_page.html', {'form': form})
