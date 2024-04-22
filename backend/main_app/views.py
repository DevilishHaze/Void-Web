from rest_framework import generics, permissions
from .models import Articles, Comments, FavoriteArticle
from .serializers import ArticleSerializer, CommentSerializer, FavoriteArticleSerializer


class ArticleListCreateRetrieveUpdateDestroyView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()


# ~~~~~~~~~~~~~~~~~Комментарии~~~~~~~~~~~~~~~~~~~

class CommentCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CommentDestroyView(generics.DestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]


# ~~~~~~~~~~~~~~~~~~Избранное~~~~~~~~~~~~~~~~~~~~~~~~

class FavoriteArticleCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
