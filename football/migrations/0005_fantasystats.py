# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-24 19:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football', '0004_userplayer'),
    ]

    operations = [
        migrations.CreateModel(
            name='FantasyStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football.Player')),
            ],
        ),
    ]
