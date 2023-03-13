# Generated by Django 4.0.6 on 2022-11-26 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connex', '0005_historique_payer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planadhesion',
            name='type_adhesion',
            field=models.CharField(choices=[('FREE', 'FREE'), ('BASIC', 'BASIC'), ('MEDIUM', 'MEDIUM'), ('PRO', 'PRO')], default='FREE', max_length=200),
        ),
    ]