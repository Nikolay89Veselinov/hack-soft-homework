from rest_framework import serializers

from repositories.models import Repository
from users.models import User


class RepositorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Repository
        fields = ['url', 'user', 'created_at']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email']
