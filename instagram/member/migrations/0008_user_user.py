# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-24 07:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0007_auto_20171023_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user',
            field=models.CharField(choices=[('F', 'Facebook'), ('D', 'Django')], default='D', max_length=1),
            preserve_default=False,
        ),
    ]