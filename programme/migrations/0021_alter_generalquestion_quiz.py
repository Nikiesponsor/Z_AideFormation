# Generated by Django 4.0.6 on 2022-11-20 01:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0020_generalquestion_generalquiz_alter_resultats_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalquestion',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Gquiz', to='programme.generalquiz'),
        ),
    ]