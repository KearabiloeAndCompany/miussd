# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-26 17:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingUssd', '0015_auto_20171126_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='contact_details',
            field=models.TextField(blank=True, default='You have not activated your account.\nDial *120*912*87*1# and Book a Demo appointment to activate.', max_length=150),
        ),
    ]
