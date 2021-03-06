# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2018-03-14 14:46
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stentor', '0006_auto_20180207_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsletter',
            name='unsubscriptions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), default=list, help_text='The subscriptions that were cancelled through this newsletter\'s "unsubscribe" link.', size=None, verbose_name='cancelled subscriptions'),
        ),
    ]
