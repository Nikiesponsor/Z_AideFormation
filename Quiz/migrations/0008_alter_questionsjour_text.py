# Generated by Django 4.1.6 on 2023-02-12 17:34

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0007_quizjour_etat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionsjour',
            name='text',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
