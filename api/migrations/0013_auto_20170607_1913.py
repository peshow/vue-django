# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-07 19:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20170606_2146'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='supervisorhost',
            unique_together=set([('host', 'project')]),
        ),
    ]
