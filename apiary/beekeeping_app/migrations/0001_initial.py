# Generated by Django 5.0.3 on 2024-04-01 21:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('contact_email', models.CharField(max_length=200)),
                ('is_published', models.BooleanField(default=False)),
                ('about', models.CharField(blank=True, max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Hive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400)),
                ('apiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beekeeping_app.apiary')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200, verbose_name='Email')),
                ('apiary', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='beekeeping_app.apiary')),
            ],
        ),
    ]