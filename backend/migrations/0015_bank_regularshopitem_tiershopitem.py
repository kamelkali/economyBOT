# Generated by Django 5.1.1 on 2025-01-11 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0014_discordusers_crime_cooldown'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('name', models.CharField(max_length=75)),
                ('number_of_user', models.BigIntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField(default='Bank name')),
                ('start_balance', models.FloatField(default=3000)),
            ],
        ),
        migrations.CreateModel(
            name='RegularShopItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TierShopItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tier', models.CharField(choices=[('II', 'Second'), ('III', 'Third'), ('IV', 'Fourth')], default='II', max_length=3)),
                ('description', models.TextField()),
            ],
        ),
    ]
