# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-22 19:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BookingUssd', '0010_ussdsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ussdsession',
            name='church',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BookingUssd.Church'),
        ),
    ]
