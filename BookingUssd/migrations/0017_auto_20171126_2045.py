# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-26 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingUssd', '0016_auto_20171126_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='update',
            name='description',
            field=models.TextField(max_length=100),
        ),
    ]
