from django.db import models

class discord_users(models.Model):
    id = models.BigIntegerField(primary_key = True)
    balance = models.FloatField()

