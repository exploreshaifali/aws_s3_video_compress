from django.core.files.base import File
from django.conf import settings
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

    # calculate resolution
    resolution = 'scale=' + width + ":-" + height
    print(resolution)

    #calculate path of folder where video is saved
    path = settings.BASE_DIR + '/compressing/'

    # compress video using ffmpeg
    p = Popen(['ffmpeg', '-i', path+uploaded_video_name,
               '-vf', resolution,
               path+'compressed_'+uploaded_video_name], stdout=PIPE, stdin=PIPE)
    p.communicate()
    print("video is compressed")

    # delete local uncompressed saved video
    delete_file(path+uploaded_video_name)

    # get the compressed video
    compressed_video = open(path+'compressed_'+uploaded_video_name, 'rb')

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
