# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 04:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_assistance_system', '0006_auto_20161028_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requirement',
            name='required_classes',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='requirement',
            name='required_hours',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
