# Generated by Django 5.0.6 on 2024-06-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_raw_weather_data_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raw_weather_data',
            name='weather_station_name',
            field=models.CharField(default=None, max_length=15),
        ),
    ]