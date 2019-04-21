# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('region_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='RentalMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('station_id', models.IntegerField(primary_key=True, serialize=False)),
                ('short_name', models.CharField(max_length=6)),
                ('name', models.CharField(max_length=100)),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('capacity', models.IntegerField()),
                ('electric_bike_surcharge_waiver', models.BooleanField()),
                ('eightd_has_key_dispenser', models.BooleanField()),
                ('has_kiosk', models.BooleanField()),
                ('region', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='apis.Region')),
                ('rental_methods', models.ManyToManyField(to='apis.RentalMethod')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duration', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('stop_time', models.DateTimeField()),
                ('bike_id', models.IntegerField()),
                ('is_subscriber', models.BooleanField()),
                ('birth_year', models.IntegerField(null=True)),
                ('gender', models.IntegerField()),
                ('start_station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='start_station_id', to='apis.Station')),
                ('stop_station', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='stop_station_id', to='apis.Station')),
            ],
        ),
    ]
