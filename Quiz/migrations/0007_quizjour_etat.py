# Generated by Django 4.1.6 on 2023-02-10 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0006_alter_resultasjour_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizjour',
            name='etat',
            field=models.CharField(blank=True, choices=[('disponible', 'disponible'), ('indisponible', 'indisponible')], max_length=200),
        ),
    ]
