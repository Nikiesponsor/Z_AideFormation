# Generated by Django 4.0.6 on 2022-11-08 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connex', '0004_alter_adherant_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historique',
            name='payer',
            field=models.BooleanField(default=False),
        ),
    ]
