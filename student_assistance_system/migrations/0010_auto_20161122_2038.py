# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 01:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_assistance_system', '0009_auto_20161119_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermajor',
            name='concentration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='student_assistance_system.RequirementSet'),
        ),
    ]
