# Generated by Django 4.0.1 on 2022-01-16 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drone_delivery', '0010_alter_medication_code_alter_medication_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalDrone',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=150, null=True, verbose_name='Slug')),
                ('serial_number', models.DecimalField(db_index=True, decimal_places=0, max_digits=100, verbose_name='Serial Number')),
                ('model', models.CharField(choices=[('Lightweight', 'Lightweight'), ('Middleweight', 'Middleweight'), ('Cruiserweight', 'Cruiserweight'), ('Heavyweight', 'Heavyweight')], max_length=13, verbose_name='Model')),
                ('weight_limit', models.DecimalField(decimal_places=2, default=500.0, max_digits=5, verbose_name='Weight Limit')),
                ('battery_capacity', models.PositiveSmallIntegerField(verbose_name='Battery Capacity')),
                ('state', models.CharField(choices=[('IDLE', 'IDLE'), ('LOADING', 'LOADING'), ('LOADED', 'LOADED'), ('DELIVERING', 'DELIVERING'), ('DELIVERED', 'DELIVERED'), ('RETURNING', 'RETURNING')], max_length=10, verbose_name='State')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Drone',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
