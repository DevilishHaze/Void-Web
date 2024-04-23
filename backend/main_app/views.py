from rest_framework import generics, permissions
from .models import Articles, Comments, FavoriteArticle
from .serializers import ArticleSerializer, CommentSerializer, FavoriteArticleSerializer


class ArticleListCreateRetrieveUpdateDestroyView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer  # просмотр,удаление,изменение,создание списка статей

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


class ArticleDetailView(generics.RetrieveAPIView):   #просмотр отдельной статьи
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer


# ~~~~~~~~~~~~~~~~~Комментарии~~~~~~~~~~~~~~~~~~~


class CommentCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):  #создавать обновлять коммы
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentDestroyView(generics.DestroyAPIView):  #удалять коммент
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentListView(generics.ListAPIView):   # просмотр списка комментариев
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

# ~~~~~~~~~~~~~~~~~~Избранное~~~~~~~~~~~~~~~~~~~~~~~~


class FavoriteArticleCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):   # удалять или создавать
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


class FavoriteArticleListView(generics.ListAPIView):  # просмотр
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FavoriteArticle.objects.filter(user=self.request.user)