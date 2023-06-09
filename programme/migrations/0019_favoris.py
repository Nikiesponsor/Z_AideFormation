# Generated by Django 4.0.6 on 2022-11-18 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programme', '0018_alter_questionquiz_text_alter_reponsesquiz_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favoris',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=200)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favoris', to='programme.matiere')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
