from rest_framework import serializers
from .models import Articles, Comments, FavoriteArticle


class ArticleSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    constellation_name = serializers.CharField(source='constellation.name_rus', read_only=True)

    class Meta:
        model = Articles
        fields = ['constellation_name', 'title', 'content','comments']
        ref_name ='ArticleSerializer'

    def get_comments(self, obj):
        comments = obj.comments.all()
        serialized_comments = CommentSerializer(comments,many=True)
        return serialized_comments.data

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

class ArticleDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = ['title', 'content','constellation']
class ArticleListSerializer(serializers.ModelSerializer):
    "Специально чтоб без комментов отображался список"
    class Meta:
        model = Articles
        fields = ['id', 'title', 'content']
class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    author = serializers.ReadOnlyField(source='author.username')
    article = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comments
        fields = ['content' , 'author' , 'article']

    def create(self , validated_data):
        # Получаем article_id из контекста
        article_id = self.context.get('article_id')

        # Извлекаем content и автора из валидированных данных
        content = validated_data['content']
        author = self.context['request'].user

        # Создаем комментарий
        comment = Comments.objects.create(
            content=content ,
            author=author ,
            article_id=article_id  # Используем article_id
        )

        return comment

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class FavoriteArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteArticle
        fields = ['user','article']
        read_only_fields = ['user']

    def create(self, validated_data):
        return FavoriteArticle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.article = validated_data.get('article', instance.article)
        instance.save()
        return instance



