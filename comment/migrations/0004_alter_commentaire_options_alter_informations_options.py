# Generated by Django 4.0.6 on 2022-11-10 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_alter_commentaire_info_alter_commentaire_nomcom'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentaire',
            options={'ordering': ['-date']},
        ),
        migrations.AlterModelOptions(
            name='informations',
            options={'ordering': ['-date']},
        ),
    ]
