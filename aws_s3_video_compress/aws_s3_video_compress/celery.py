from __future__ import absolute_import

import os
import celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aws_s3_video_compress.settings')

app = celery.Celery('aws_s3_video_compress')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
