from rest_framework import permissions
from rest_framework import serializers

from .models import Constellation
from ..main_app.models import Articles

class ConstellationForAdmin(serializers.ModelSerializer):
    permission_classes = permissions.IsAdminUser
    article_url = serializers.SerializerMethodField()
    class Meta:
        model = Constellation
        fields = ['id','name','name_rus', 'ra', 'dec','article_url','image_url']

    def get_article_url(self , obj):
            request = self.context.get('request')
            try:
                article = Articles.objects.get(constellation=obj)
                return request.build_absolute_uri(f'/articles/{article.id}/')
            except Articles.DoesNotExist:
                return None
class ConstellationSerializer(serializers.ModelSerializer):
    article_url = serializers.SerializerMethodField()

    class Meta:
        model = Constellation
        fields = ['name_rus', 'ra', 'dec','article_url', 'image_url']

    def get_article_url(self, obj):
        request = self.context.get('request')
        try:
            article = Articles.objects.get(constellation=obj)
            return request.build_absolute_uri(f'/articles/{article.id}/')
        except Articles.DoesNotExist:
            return None

class CoordinateSerializer(serializers.Serializer):
    longitude = serializers.FloatField(required=True)
    latitude = serializers.FloatField(required=True)

