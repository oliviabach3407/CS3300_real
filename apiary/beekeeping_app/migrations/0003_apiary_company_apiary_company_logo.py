# Generated by Django 5.0.3 on 2024-04-02 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beekeeping_app', '0002_rename_user_keeper'),
    ]

    operations = [
        migrations.AddField(
            model_name='apiary',
            name='company',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='apiary',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='company_logos/'),
        ),
    ]