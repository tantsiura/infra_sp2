from django.forms import ModelForm

from .models import (CategoryImport, CommentImport, GenreImport, ReviewImport,
                     TitleImport)


class CategoryImportForm(ModelForm):
    class Meta:
        model = CategoryImport
        fields = ('csv_file',)


class GenreImportForm(ModelForm):
    class Meta:
        model = GenreImport
        fields = ('csv_file',)


class TitleImportForm(ModelForm):
    class Meta:
        model = TitleImport
        fields = ('csv_file',)


class ReviewImportForm(ModelForm):
    class Meta:
        model = ReviewImport
        fields = ('csv_file',)


class CommentImportForm(ModelForm):
    class Meta:
        model = CommentImport
        fields = ('csv_file',)
