# Generated by Django 4.0.1 on 2022-01-13 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drone_delivery', '0004_deliverypackage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverypackage',
            name='drone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone_delivery.drone', verbose_name='Assigned Drone'),
        ),
        migrations.AlterField(
            model_name='deliverypackage',
            name='medications',
            field=models.ManyToManyField(to='drone_delivery.Medication', verbose_name='Medications Items'),
        ),
    ]
