from django.db import models

class discord_users(models.Model):
    id = models.BigIntegerField(primary_key = True)
    balance = models.FloatField()

class work(models.Model):
    id = models.AutoField(primary_key = True)
    text = models.TextField()
    money = models.FloatField()

class jail(models.Model):
    user_id = models.BigIntegerField
    bust_time = models.DateTimeField()
    fee = models.FloatField()
    release_time = models.DateTimeField()

