# aws_s3_video_compress

A simple utility that allows to upload video on AWS Simple Storage Service(S3), provide specifications(video resolution and its audio frequency) to compress video and store compressed video as well on S3 such that next who want to see the video will able to download the compressed videos.

It uses postgreSQL as database, AWS S3 to store videos, ffmpeg to compress videos and redis for caching compress task.

##How it works?
  1. User upload video and provide specifications to compress it.
  1. Uncompressed video get saved on S3.
  1. At the same time it also get save on server disk.
  1. After that a task(that contain specification given by user, video name and primary key of above stored object) is send to queue(amqp) to compress video .
  1. Video gets compress using ffmpeg library.
  1. Lastly compressed video gets saved on S3 and same object is updated in database.

##Setup for developers
--------------------

1. Make sure you have installed Python 2.7.6, [pip](https://pip.pypa.io/en/latest/) and [virtualenv](http://www.virtualenv.org/en/latest/).
1. Make sure you have PostgreSQL, Redis, ffmpeg installed.
1. Make sure you have a bucket on AWS S3 and keys to access it.
1. Clone the repo -`https://github.com/exploreshaifali/aws_s3_video_compress.git` and cd into the `aws_s3_video_compress` directory.
1. Create a virtual environment with Python 2 and install dependencies:

 ```bash
 $ virtualenv venv
 $ source venv/bin/activate
 $ pip install -r requirements.txt
 ```
1. Create `video_compress_db` database, where `video_compress_db` might be any suitable name.
1. Fill in the database details in `aws_s3_video_compress/settings.py`.
1. Run `export SECRET_KEY=foobarbaz` in your terminal, ideally the secret key
  should be 40 characters long, unique and unpredictable. Optionally to set the
  shell variable every time you activate the virtualenv, edit `venv/bin/activate`
  and add to the bottom the export statement.
1. Similarly set `DEFAULT_FILE_STORAGE`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME` for your AWS S3 in `aws_s3_video_compress/settings.py` and update `BROKER_URL`, `CELERY_RESULT_BACKEND` for django-celery. Default celery settings will be 'redis://127.0.0.1:6379/0' .
1. Run `python manage.py migrate`.
1. Run `python manage.py createsuperuser` to create a superuser for the admin panel.
  Fill in the details asked.
1. Run `python manage.py runserver` to start the development server.
