# Generated by Django 5.1.4 on 2025-01-12 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('color_identity', models.CharField(max_length=10)),
                ('card_type', models.CharField(max_length=120)),
                ('rarity', models.CharField(max_length=50)),
                ('mtg_set', models.CharField(max_length=3)),
                ('text', models.TextField(max_length=2000)),
                ('image_url', models.URLField(max_length=1000)),
            ],
        ),
    ]
