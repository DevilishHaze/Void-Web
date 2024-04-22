from rest_framework import serializers
from .models import Articles, Comments, FavoriteArticle


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Articles
        fields = '__all__'

    def create(self, validated_data):
        return Articles.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

    def create(self, validated_data):
        return Comments.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment_text = validated_data.get('comment_text', instance.comment_text)
        instance.save()
        return instance


class FavoriteArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteArticle
        fields = '__all__'

    def create(self, validated_data):
        return FavoriteArticle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.article = validated_data.get('article', instance.article)
        instance.save()
        return instance
