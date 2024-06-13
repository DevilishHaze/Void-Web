from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username','password']
        ref_name = 'UserSerializer'
class UserWithoutPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']
        read_only_fields = fields
