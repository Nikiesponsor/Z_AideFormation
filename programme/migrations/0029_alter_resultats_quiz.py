# Generated by Django 4.1.6 on 2023-02-08 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0028_generalquestion_indication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultats',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizmodule', to='programme.quiz'),
        ),
    ]
