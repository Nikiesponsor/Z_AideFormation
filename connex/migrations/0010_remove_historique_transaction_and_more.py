# Generated by Django 4.1.7 on 2023-03-13 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connex', '0009_historique_transaction_alter_historique_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historique',
            name='transaction',
        ),
        migrations.AddField(
            model_name='historique',
            name='transaction_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]