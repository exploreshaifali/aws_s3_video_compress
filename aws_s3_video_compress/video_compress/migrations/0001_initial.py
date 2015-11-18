# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('video', models.FileField(upload_to=b'zaya-videos')),
                ('title', models.CharField(unique=True, max_length=200)),
                ('time', models.DateTimeField()),
                ('compressed_video', models.FileField(upload_to=b'zaya-videos', blank=True)),
            ],
        ),
    ]
