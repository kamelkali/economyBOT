# Generated by Django 5.1.1 on 2024-12-18 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_discordusers_work_cooldown'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='title',
        ),
    ]
