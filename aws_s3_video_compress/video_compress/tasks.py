from django.core.files.base import File
from subprocess import Popen, PIPE

from aws_s3_video_compress.celery import app
from video_compress.models import Video

@app.task
def hello_task():
    print('hello world!')

@app.task
def video_compress_task(uploaded_video_name, object_id, width, height, audio_frequency):
    """Compress the video and save on s3"""
    print("in the video_compress_task")

    #Error coming here!
    # import pdb
    # pdb.set_trace()
    # from celery.contrib import rdb
    # rdb.set_trace()
    print(uploaded_video_name)
    print object_id
    print width
    # calculate resolution
    resolution = 'scale=' + width + ":-" + height
    print resolution

    # compress video using ffmpeg
    p = Popen(['ffmpeg', '-i', "./compressing/"+uploaded_video_name,
               '-vf', resolution,
               './compressing/compressed_'+uploaded_video_name], stdout=PIPE, stdin=PIPE)
    p.communicate()
    print("video is compressed")

    # delete local uncompressed saved video
    delete_file("./compressing/"+uploaded_video_name)

    # get the compressed video
    compressed_video = open('./compressing/compressed_'+uploaded_video_name, 'rb')

    # get saved object from database to update with compressed video
    print("Now actually saving compressed video.")
    object = Video.objects.get(pk=object_id)
    object.compressed_video = File(compressed_video)
    object.save()
    print("your compressed video is saved! Celebrate :D")

    # delete compressed video from server disk
    delete_file('./compressing/compressed_'+uploaded_video_name)


def delete_file(file_path):
    """Delete file from server disk"""
    p = Popen(['rm', file_path])
    p.communicate()
    print(file_path, " file deleted.")
