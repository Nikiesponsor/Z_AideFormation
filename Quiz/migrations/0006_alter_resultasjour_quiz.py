# Generated by Django 4.1.6 on 2023-02-03 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0005_questionsjour_indication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultasjour',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='JourReQuiz', to='Quiz.quizjour'),
        ),
    ]
