from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, get_token,
                       registration)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
v1_router.register('users', UserViewSet, basename='users')

v1_auth_urlpatterns = [
    path('auth/signup/', registration, name='signup'),
    path('auth/token/', get_token, name='token'),
]

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include(v1_auth_urlpatterns)),
]
