from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
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

    def retrieve(self , request , *args , **kwargs):  #получение одной статьи и комментов к ней
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        comments = Comments.objects.filter(article=instance)
        comments_serializer = CommentSerializer(comments , many=True)
        data = serializer.data
        data['comments'] = comments_serializer.data
        return Response(data)
    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save(author=self.request.user)
        else:
            raise PermissionDenied("Only admins can create articles.\nТолько админы могут создавать статьи")


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action  in ['update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsOwnerOrAdminPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]


class FavoriteArticleViewSet(viewsets.ModelViewSet):
    queryset = FavoriteArticle.objects.all()
    serializer_class = FavoriteArticleSerializer
    permission_classes = [permissions.IsOwnerOrAdminPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        if instance.user == self.request.user:
            instance.delete()

    @action(detail=True, methods=['post'])
    def add_to_favorites(self, request, pk=None):
        article = self.get_object()
        if FavoriteArticle.objects.filter(user=request.user, article=article).exists():
            return Response({"message": "Article already in favorites."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={"article": article.id})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # @action(detail=True, methods=['get'])
    # def view_article(self,request,pk=None):
    #     fav_article = self.get_object()
