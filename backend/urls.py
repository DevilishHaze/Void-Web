"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path , include , re_path
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from backend.main_app.views import CommentAPIView , ArticleListAPIView , \
    CommentListApiView , ArticleUpdateAPIView , UserCommentListAPIView , FavoriteArticleAPIView , AddToFavoritesAPIView
from backend.users.views import UserViewSet
from .yasg import urlpatterns as doc_urls
#router = DefaultRouter()

#router.register('api/articles', ArticleViewSet)
#router.register('api/comments', CommentViewSet)
#router.register('api/fav-articles', FavoriteArticleViewSet, basename='fav-article')
#router.register('api/users', UserViewSet, basename='user')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('articles/' , ArticleListAPIView.as_view() , name='article-list') ,
    path('articles/<int:pk>/' , ArticleUpdateAPIView.as_view() , name='article-update') ,
    path('comments/' , CommentListApiView.as_view() , name='comment-list') ,
    path('comments/<int:pk>/' , CommentAPIView.as_view() , name='comment-detail') ,
    path('articles/<int:article_id>/comments/', UserCommentListAPIView.as_view(), name='user-comment-list'),
    path('favorites/' , FavoriteArticleAPIView.as_view() , name='favorite-article') ,
    path('favorites/<int:pk>/' , FavoriteArticleAPIView.as_view() , name='favorite-article-detail') ,
    path('articles/<int:pk>/add_to_favorites/', AddToFavoritesAPIView.as_view(), name='add-to-favorites'),
     ]

urlpatterns += doc_urls