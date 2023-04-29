from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer,
    TitleCreateUpdateSerializer, GenreSerializer, ReviewSerializers,
    CommentSerializers, UserSerializer, EmailSerializer, TokenSerializer)
from api.permissions import (
    IsAdminUserOrReadOnly, IsAdmin, IsAuthorModeratorAdminOrReadOnly,)
from api.mixins import CreateListDeleteViewSet
from api.filters import TitleFilter
from reviews.models import Category, Genre, Title, Review
from users.models import User


class CategoryViewSet(CreateListDeleteViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDeleteViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleCreateUpdateSerializer
        return TitleSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def registration(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data.get('email')
    username = serializer.validated_data.get('username')
    if username == 'me':
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        user, created = User.objects.get_or_create(
            email=email,
            username=username
        )
    except Exception as error:
        return Response(
            f'Произошла ошибка ->{error}<-',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация YaMDB',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='from@example.com',
        recipient_list=[email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    user = get_object_or_404(User, username=username)
    confirmation_code = serializer.validated_data.get('confirmation_code')
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response({'token': token}, status=status.HTTP_200_OK)
    return Response(
        {'confirmation_code': confirmation_code},
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    # метод для предотвращения PUT-запроса
    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.is_admin:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'error': 'Вы не авторизованы для выполнения этого действия.'},
                status=status.HTTP_403_FORBIDDEN
            )

    @action(
        methods=['patch', 'get'],
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_path='me',
        url_name='me'
    )
    def me(self, request):
        user = request.user
        if self.request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=user.role, partial=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializers
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = (IsAuthorModeratorAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)
