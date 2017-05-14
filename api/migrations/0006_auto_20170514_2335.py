# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-14 23:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20170514_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='host_id',
        ),
        migrations.RemoveField(
            model_name='jobmessage',
            name='job_id',
        ),
        migrations.DeleteModel(
            name='Login',
        ),
        migrations.RemoveField(
            model_name='remote',
            name='host_id',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='JobMessage',
        ),
        migrations.DeleteModel(
            name='Remote',
        ),
        migrations.DeleteModel(
            name='RemoteHost',
        ),
    ]