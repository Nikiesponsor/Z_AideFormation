# Generated by Django 4.0.6 on 2022-12-14 09:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programme', '0023_alter_matiere_favoris'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecons',
            name='Favoris',
            field=models.ManyToManyField(blank=True, null=True, related_name='favoris', to=settings.AUTH_USER_MODEL),
        ),
    ]
