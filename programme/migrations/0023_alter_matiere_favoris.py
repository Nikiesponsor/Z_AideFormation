# Generated by Django 4.0.6 on 2022-11-26 01:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programme', '0022_matiere_favoris_delete_favoris'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matiere',
            name='favoris',
            field=models.ManyToManyField(blank=True, null=True, related_name='favori', to=settings.AUTH_USER_MODEL),
        ),
    ]
