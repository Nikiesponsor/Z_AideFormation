# Generated by Django 4.0.6 on 2022-11-14 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0015_remove_questionquiz_contenue'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionquiz',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reponsesquiz',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]