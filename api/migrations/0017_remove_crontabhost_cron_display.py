# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-16 16:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_auto_20170611_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crontabhost',
            name='cron_display',
        ),
    ]
