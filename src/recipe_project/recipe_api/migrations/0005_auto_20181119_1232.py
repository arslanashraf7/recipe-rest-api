# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 12:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_api', '0004_followingsmodel'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='followingsmodel',
            unique_together=set([('follower', 'followed')]),
        ),
    ]