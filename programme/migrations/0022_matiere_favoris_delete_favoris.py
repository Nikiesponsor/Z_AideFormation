# Generated by Django 4.0.6 on 2022-11-26 01:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programme', '0021_alter_generalquestion_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='matiere',
            name='favoris',
            field=models.ManyToManyField(blank=True, default=None, related_name='favori', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Favoris',
        ),
    ]
