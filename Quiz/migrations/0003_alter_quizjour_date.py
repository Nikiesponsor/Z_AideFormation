# Generated by Django 4.0.6 on 2022-12-13 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0002_alter_quizjour_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizjour',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
