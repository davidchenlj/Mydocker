# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='containers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('containers_id', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('command', models.CharField(max_length=255)),
                ('images', models.CharField(max_length=255)),
                ('host', models.CharField(max_length=255)),
                ('create_time', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='docker_vm',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docker_addr', models.CharField(unique=True, max_length=255)),
                ('docker_name', models.CharField(max_length=255)),
                ('docker_version', models.CharField(max_length=255)),
            ],
        ),
    ]
