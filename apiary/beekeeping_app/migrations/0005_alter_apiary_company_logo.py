# Generated by Django 5.0.3 on 2024-04-02 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beekeeping_app', '0004_alter_apiary_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiary',
            name='company_logo',
            field=models.ImageField(blank=True, null=True, upload_to='C:/Users/olivi/OneDrive/GitHub/CS3300_real/apiary/static/images/company_logos/'),
        ),
    ]
