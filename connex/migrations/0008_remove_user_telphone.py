# Generated by Django 4.1.6 on 2023-02-09 14:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connex', '0007_user_ceckbox_info'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='telphone',
        ),
    ]