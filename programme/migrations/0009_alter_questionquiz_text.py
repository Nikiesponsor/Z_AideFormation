# Generated by Django 4.0.6 on 2022-11-14 09:29

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0008_alter_questionquiz_text_alter_reponsesquiz_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionquiz',
            name='text',
            field=django_quill.fields.QuillField(blank=True, default='pipo', null=True),
        ),
    ]