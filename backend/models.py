from django.utils import timezone
from django.db import models

class DiscordUsers(models.Model):
    id = models.BigIntegerField(primary_key = True)
    balance = models.FloatField()
    work_cooldown = models.DateTimeField(default=timezone.now)
    crime_cooldown = models.DateTimeField(default=timezone.now)
    class Tier(models.TextChoices):
        FIRST = "I"
        SECOND = "II"
        THIRD = "III"
        FOURTH = "IV"

    tier = models.CharField(
            max_length=3,
            choices=Tier.choices,
            default=Tier.FIRST,
    )
    wallet_create_date = models.DateTimeField(auto_now_add=True)
    discord_name = models.CharField(max_length=50, null=True)

class Work(models.Model):

    class Tier(models.TextChoices):
        FIRST = "I"
        SECOND = "II"
        THIRD = "III"
        FOURTH = "IV"

    work_id = models.AutoField(primary_key = True)
    description = models.TextField(default="Description")
    tier = models.CharField(
        max_length=3,
        choices = Tier.choices,
        default = Tier.FIRST,
    )
    balance = models.FloatField(default=0.0)


class Bank(models.Model):
    name = models.CharField(max_length=75)
    number_of_user = models.BigIntegerField(primary_key=True)
    description = models.TextField(default="Bank name")
    start_balance = models.FloatField(default=3000)


class Jail(models.Model):
    user_id = models.BigIntegerField
    bust_time = models.DateTimeField()
    fee = models.FloatField()
    release_time = models.DateTimeField()


class Transaction(models.Model):
    payer_id = models.BigIntegerField()
    payee_id = models.BigIntegerField()
    balance = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class RegularShopItem(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField(default=0.0)
    description = models.TextField()

class TierShopItem(models.Model):
    name = models.CharField(max_length=50)
    cost = models.FloatField(default=0.0)

    class Tier(models.TextChoices):
        SECOND = "II"
        THIRD = "III"
        FOURTH = "IV"
    tier = models.CharField(
        max_length=3,
        choices=Tier.choices,
        default=Tier.SECOND,
    )
    description = models.TextField()
