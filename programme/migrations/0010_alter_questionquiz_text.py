# Generated by Django 4.0.6 on 2022-11-14 09:31

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0009_alter_questionquiz_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionquiz',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
