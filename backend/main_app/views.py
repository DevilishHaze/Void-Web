from rest_framework import viewsets, permissions
from .models import Articles, Comments, FavoriteArticle
from .serializers import ArticleSerializer, CommentSerializer, FavoriteArticleSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Articles.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class FavoriteArticleViewSet(viewsets.ModelViewSet):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return FavoriteArticle.objects.filter(user=user)
        else:
            return FavoriteArticle.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()

# class ArticleListCreateRetrieveUpdateDestroyView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
#     queryset = Articles.objects.all()
#     serializer_class = ArticleSerializer  # просмотр,удаление,изменение,создание списка статей
#
#     def get_permissions(self):
#         if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
#             self.permission_classes = [permissions.IsAdminUser]
#         else:
#             self.permission_classes = [permissions.AllowAny]
#         return super().get_permissions()
#
#
# class ArticleDetailView(generics.RetrieveAPIView):   #просмотр отдельной статьи
#     queryset = Articles.objects.all()
#     serializer_class = ArticleSerializer
#
#
# # ~~~~~~~~~~~~~~~~~Комментарии~~~~~~~~~~~~~~~~~~~
#
#
# class CommentCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):  #создавать обновлять коммы
#     queryset = Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# class CommentDestroyView(generics.DestroyAPIView):  #удалять коммент
#     queryset = Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.IsAdminUser]
#
#
# class CommentListView(generics.ListAPIView):   # просмотр списка комментариев
#     queryset = Comments.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.AllowAny]
#
# # ~~~~~~~~~~~~~~~~~~Избранное~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# class FavoriteArticleCreateDestroyView(generics.CreateAPIView, generics.DestroyAPIView):   # удалять или создавать
#     queryset = FavoriteArticle.objects.all()
#     serializer_class = FavoriteArticleSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class FavoriteArticleListView(generics.ListAPIView):  # просмотр
#     queryset = FavoriteArticle.objects.all()
#     serializer_class = FavoriteArticleSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         return FavoriteArticle.objects.filter(user=self.request.user)