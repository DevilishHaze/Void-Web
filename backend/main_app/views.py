from sqlite3 import IntegrityError
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Articles, Comments, FavoriteArticle

from .serializers import ArticleSerializer , CommentSerializer , FavoriteArticleSerializer , ArticleListSerializer , \
    ArticleDetailSerializer


class ArticleListAPIView(generics.ListCreateAPIView):
    """Список статей получение или создание статьи"""
    queryset = Articles.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return ArticleDetailSerializer  # Используем детализированный сериализатор для создания и редактирования
        return ArticleListSerializer  # Используем список сериализатор для просмотра

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [permissions.IsAdminUser]  # Только администраторы могут редактировать и создавать
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Все могут просматривать
        return super().get_permissions()

    def get_queryset(self):
        return Articles.objects.all()


class ArticleUpdateAPIView(generics.UpdateAPIView):
    """"Редактирование статьи или получение одной статьи"""
    queryset = Articles.objects.all()
    serializer_class = ArticleDetailSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdminUser]

    def get(self , request , pk=None):
        if pk is not None:
            article = get_object_or_404(Articles , pk=pk)
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        else:
            queryset = Articles.objects.all()
            serializer = ArticleSerializer(queryset , many=True)
            return Response(serializer.data)
    def perform_update(self, serializer):
        serializer.save(author=self.request.user)
class CommentListApiView(generics.ListAPIView):
    """"Список комментов к  видят админы(добавление,получение,редактирование)"""
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAdminUser]
def get_queryset(self):
    article_id = self.kwargs.get('article_id')
    return Comments.objects.filter(article_id=article_id)


def perform_create(self, serializer):
    serializer.save(user=self.request.user)

class UserCommentListAPIView(generics.ListCreateAPIView):
    """"Список комментов к одной статье видят все(добавление,получение,редактирование)"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'article_id'

    def get_queryset(self):
        article_id = self.kwargs.get('article_id')
        return Comments.objects.filter(article_id=article_id)

    def get_serializer_context(self):
        # Передаем article_id в контекст сериализатора
        context = super().get_serializer_context()
        context['article_id'] = self.kwargs.get('article_id')
        return context

class CommentAPIView(APIView):
    """"Удаление коммента или получение комментов"""
    permission_classes = [permissions.AllowAny]


    def get(self, request, pk=None):
        if pk:
            comment = get_object_or_404(Comments, pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        else:
            queryset = Comments.objects.all()
            serializer = CommentSerializer(queryset, many=True)
            return Response(serializer.data)

    def delete(self, request, pk):
        comment = get_object_or_404(Comments, pk=pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteArticleAPIView(APIView):
        permission_classes = [permissions.IsAdminOrOwnerPermission]

        def post(self , request):
            data = request.data.copy()
            data['user'] = request.user.id  # Добавляем текущего пользователя в данные запроса
            serializer = FavoriteArticleSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

        def delete(self , request , pk):
            favorite_article = get_object_or_404(FavoriteArticle , pk=pk)
            if favorite_article.user != request.user:
                return Response({"error": "You can only delete your own favorites."} , status=status.HTTP_403_FORBIDDEN)
            favorite_article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class AddToFavoritesAPIView(APIView):
    """" Добавление в избранное статьи"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self , request , pk):
        article = get_object_or_404(Articles , pk=pk)
        user = request.user
        try:
            favorite_article = FavoriteArticle.objects.get(user=user , article=article)
            return Response({"error": "Article already in favorites."} , status=status.HTTP_400_BAD_REQUEST)
        except FavoriteArticle.DoesNotExist:
            serializer = FavoriteArticleSerializer(data={"article": article.pk})
            if serializer.is_valid():
                serializer.save(user=user)  # Сохраняем с текущим пользователем
                return Response(serializer.data , status=status.HTTP_201_CREATED)
            return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "Unable to add article to favorites."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewFavoritesAPIView(generics.ListAPIView):
    serializer_class = FavoriteArticleSerializer
    permission_classes = [permissions.IsAdminOrOwnerPermission]

    def get_queryset(self):
        return FavoriteArticle.objects.filter(user=self.request.user)

class RemoveFromFavoritesAPIView(generics.DestroyAPIView):
        queryset = FavoriteArticle.objects.all()
        serializer_class = FavoriteArticleSerializer
        permission_classes = [permissions.IsAdminOrOwnerPermission]

        def delete(self , request , *args , **kwargs):
            user = request.user
            favorite_article = self.get_object()
            if favorite_article.user != user:
                return Response({"error": "You can only remove articles from your own favorites."} ,
                                status=status.HTTP_403_FORBIDDEN)
            favorite_article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)