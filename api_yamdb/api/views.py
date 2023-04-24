from api.filters import TitleFilter
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             SignUpSerializer, TitleSerializerCreateAndUpdate,
                             TitleSerializerGet, TokenSerializer,
                             UserEditSerializer, UserSerializer)
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api_yamdb.settings import DEFAULT_EMAIL

from .permissions import (AuthorAdminModeratorOrReadOnly, IsAdminOnly,
                          IsAdminOrReadOnly)


class CategoryAndGenreMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Class for categories and genres."""

    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'


class CategoryViewSet(CategoryAndGenreMixin):
    """Class for working with categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class GenreViewSet(CategoryAndGenreMixin):
    """Class for working with genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Class for working with works."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    http_method_names = ['get', 'post', 'delete', 'patch']
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        """Re-define method to choose a proper serializer."""
        if self.action in ['create', 'partial_update', 'destroy']:

            return TitleSerializerCreateAndUpdate

        return TitleSerializerGet


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing reviews.
    The viewset provides re-defined `perform_create()` and `get_queryset()`
    actions.
    """
    serializer_class = ReviewSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        """Re-define method to return only reviews belonging to the post."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))

        return title.reviews.select_related('author')

    def perform_create(self, serializer):
        """Re-define method to set review's author and title automatically."""
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user,
            title=title
        )


class CommentViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for managing comments.
    The viewset provides re-defined `perform_create()` and `get_queryset()`
    actions.
    """
    serializer_class = CommentSerializer
    permission_classes = [AuthorAdminModeratorOrReadOnly]

    def get_queryset(self):
        """Re-define method to return only comments belonging to the post."""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))

        return review.comments.select_related('author')

    def perform_create(self, serializer):
        """Re-define method to set comment's author and post automatically."""
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(
            author=self.request.user,
            review=review
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_user(request):
    """Re-define method to sign up"""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, create = User.objects.get_or_create(
            **serializer.validated_data)
    except IntegrityError:

        return Response(
            'Ошибка данных. Проверьте поле login или email!',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    user.save()
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Код подтверждения:{confirmation_code}',
        from_email=DEFAULT_EMAIL,
        recipient_list=[user.email],
    )

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_token(request):
    """Re-define method to create token"""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)

        return Response(
            {'token': f'{token}'},
            status=status.HTTP_200_OK
        )

    return Response(
        {'message': 'Пользователь не обнаружен'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for managing users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ('username',)
    lookup_field = ('username')
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    permission_classes = [IsAdminOnly]
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def edit_own_profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
