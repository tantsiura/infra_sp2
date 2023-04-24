from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    """Class for converting category data."""

    class Meta:
        model = Category
        fields = (
            'name',
            'slug',
        )


class GenreSerializer(serializers.ModelSerializer):
    """Class for converting genre data."""

    class Meta:
        model = Genre
        fields = (
            'name',
            'slug',
        )


class TitleSerializerGet(serializers.ModelSerializer):
    """Class for converting product data with the GET method."""

    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('rating',)


class TitleSerializerCreateAndUpdate(serializers.ModelSerializer):
    """
    Class for converting product data in the CREATE and UPDATE methods.
    """

    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        """Validate that the year value is correct."""
        now = timezone.now().year
        if value > now:
            raise serializers.ValidationError(
                '"year" не может быть позднее текущего года.'
            )

        return value


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review instances.
    """

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )
        read_only_fields = ('author',)

    def validate(self, data):
        """Validate the unique author and title pair."""
        if self.context['request'].method == 'POST' and Review.objects.filter(
            title_id=self.context['view'].kwargs.get('title_id'),
            author=self.context['request'].user
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв на это произведение.'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment instances.
    """
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User instances.
    """
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким именем уже существует.'
            )
        ])
    email = serializers.EmailField(
        max_length=254,
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Пользователь с таким email-адресом уже существует.'
            )
        ]
    )

    class Meta:
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        model = User
        lookup_field = 'username'


class UserEditSerializer(UserSerializer):
    """
    Serializer for Me instances.
    """
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    """
    Serializer for Signing up.
    """
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        """Validate that the username can't have value 'me'."""
        if value == 'me':
            raise serializers.ValidationError(
                '"me" не может быть использован в качестве Username!'
            )

        return value

    def validate(self, data):
        """
        Validate username and email.
        If email and username match then API gives another token.
        If eiher email or username already exists
        then API gives Validation Error.
        """
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():

            return data

        if User.objects.filter(
                Q(username__iexact=data['username'])
                | Q(email__iexact=data['email'])
        ):
            raise serializers.ValidationError(
                'Пользователь с таким именем или email существует'
            )

        return data


class TokenSerializer(serializers.Serializer):
    """
    Serializer for Creating Token.
    """
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
