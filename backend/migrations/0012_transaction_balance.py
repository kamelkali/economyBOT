# Generated by Django 5.1.1 on 2025-01-02 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0011_transaction_discordusers_discord_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='balance',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
