# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-15 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20170514_2346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supervisorhost',
            old_name='hostname',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='supervisorhost',
            name='supervisor_project',
        ),
        migrations.AddField(
            model_name='supervisorhost',
            name='describe',
            field=models.TextField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='supervisorhost',
            name='project',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='supervisorhost',
            name='ip',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='supervisorhost',
            name='name',
            field=models.CharField(default='空', max_length=100),
        ),
    ]