from .models import discord_users
from rest_framework.serializers import ModelSerializer

class Discord_user_serializers(ModelSerializer):
    class Meta:
        model = discord_users
        fields = '__all__'
    def create(self, validated_data):
        user = discord_users.objects.create(**validated_data)
        return user
