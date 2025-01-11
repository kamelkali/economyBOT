from .models import DiscordUsers, Work, Transaction, RegularShopItem, TierShopItem
from rest_framework.serializers import ModelSerializer

class DiscordUsersSerialisers(ModelSerializer):
    class Meta:
        model = DiscordUsers
        fields = '__all__'
    def create(self, validated_data):
        user = DiscordUsers.objects.create(**validated_data)
        return user

class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'

class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
    def create(self, validated_data):
        transaction = Transaction.objects.create(**validated_data)
        return transaction


class RegularItemsSerializer(ModelSerializer):
    class Meta:
        model = RegularShopItem
        fields = '__all__'

class TierItemsSerializer(ModelSerializer):
    class Meta:
        model = TierShopItem
        fields = '__all__'
