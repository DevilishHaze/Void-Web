from django.urls import path
from . import views

urlpatterns = [
    path('api/articles/', views.ArticleListCreateRetrieveUpdateDestroyView.as_view() , name='article-list-multi') ,
    path('api/articles/<int:pk>/', views.ArticleDetailView.as_view(), name='article-detail') ,
    path('api/comments/', views.CommentCreateUpdateView.as_view(), name='com-create-update') ,
    path('api/comments/<int:pk>/', views.CommentDestroyView.as_view(), name='com-del') ,
    path('api/favorite-articles/', views.FavoriteArticleCreateDestroyView.as_view(),name='favarticle-create-del') ,
    path('api/favorite-articles/<int:pk>/', views.FavoriteArticleListView.as_view(), name='favarticle-list') ,

]