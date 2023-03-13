# Generated by Django 4.0.6 on 2022-11-07 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connex', '0003_adherant_planadhesion_souscription_historique_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherant',
            name='token',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='planadhesion',
            name='type_adhesion',
            field=models.CharField(choices=[('FREE', 'FREE'), ('BASIC', 'BASIC'), ('BASICPLUS', 'BASICPLUS'), ('MEDIUM', 'MEDIUM'), ('PRO', 'PRO'), ('PROPLUS', 'PROPLUS')], default='FREE', max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, default='', max_length=100, null=True, verbose_name='Username'),
        ),
    ]