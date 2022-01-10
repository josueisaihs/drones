# Generated by Django 4.0.1 on 2022-01-10 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, verbose_name='Slug')),
                ('serial_number', models.DecimalField(decimal_places=0, max_digits=100, unique=True, verbose_name='Serial Number')),
                ('model', models.CharField(choices=[('Lightweight', 'Lightweight'), ('Middleweight', 'Middleweight'), ('Cruiserweight', 'Middleweight'), ('Heavyweight', 'Middleweight')], max_length=13, verbose_name='Model')),
                ('weight_limit', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Weight Limit')),
                ('battery_capacity', models.PositiveSmallIntegerField(verbose_name='Battery Capacity')),
                ('state', models.CharField(choices=[('IDLE', 'IDLE'), ('LOADING', 'LOADING'), ('LOADED', 'LOADED'), ('DELIVERING', 'DELIVERING'), ('DELIVERED', 'DELIVERED'), ('RETURNING', 'RETURNING')], max_length=10, verbose_name='State')),
            ],
            options={
                'verbose_name': 'Drone',
                'verbose_name_plural': 'Drones',
            },
        ),
    ]
