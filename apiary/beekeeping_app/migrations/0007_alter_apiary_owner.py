# Generated by Django 5.0.3 on 2024-04-20 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beekeeping_app', '0006_apiary_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiary',
            name='owner',
            field=models.CharField(max_length=200),
        ),
    ]
