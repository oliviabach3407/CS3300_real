# Generated by Django 5.0.3 on 2024-04-21 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beekeeping_app', '0009_alter_keeper_apiary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hive', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to='beekeeping_app.hive')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('calendar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='beekeeping_app.calendar')),
            ],
        ),
    ]
