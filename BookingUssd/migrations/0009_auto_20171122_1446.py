# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-11-22 12:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BookingUssd', '0008_auto_20171122_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='church',
            name='booking_message_label',
            field=models.TextField(blank=True, default='When and where?', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='church',
            name='booking_submission_message',
            field=models.TextField(blank=True, default='Thank you for submitting your request. We will be intouch shortly.', max_length=150, null=True),
        ),
    ]