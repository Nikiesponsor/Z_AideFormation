# Generated by Django 4.0.6 on 2022-11-07 01:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('connex', '0002_remove_user_bio_remove_user_country_user_telphone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adherant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='PlanAdhesion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_adhesion', models.CharField(choices=[('BASIC', 'BASIC'), ('BASICPLUS', 'BASICPLUS'), ('MEDIUM', 'MEDIUM'), ('PRO', 'PRO'), ('PROPLUS', 'PROPLUS')], max_length=200)),
                ('dure', models.PositiveIntegerField()),
                ('prix', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Souscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_expiration', models.DateField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('adherant_souscrit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='souscription', to='connex.adherant')),
            ],
        ),
        migrations.CreateModel(
            name='Historique',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prix', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('token', models.CharField(max_length=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('typelan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='connex.planadhesion')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='adherant',
            name='typeplan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='connex.planadhesion'),
        ),
        migrations.AddField(
            model_name='adherant',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='adherant', to=settings.AUTH_USER_MODEL),
        ),
    ]
