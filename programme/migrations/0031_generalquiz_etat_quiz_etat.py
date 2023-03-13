# Generated by Django 4.1.6 on 2023-02-19 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0030_alter_generalresultats_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalquiz',
            name='etat',
            field=models.CharField(blank=True, choices=[('disponible', 'disponible'), ('indisponible', 'indisponible')], max_length=200),
        ),
        migrations.AddField(
            model_name='quiz',
            name='etat',
            field=models.CharField(blank=True, choices=[('disponible', 'disponible'), ('indisponible', 'indisponible')], max_length=200),
        ),
    ]