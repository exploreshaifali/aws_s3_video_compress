from video_compress.models import Video
from video_compress.serializers import VideoSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from django.shortcuts import render
from django.conf import settings
from datetime import datetime

from video_compress.forms import VideoForm
from video_compress.tasks import video_compress_task, hello_task


class VideoList(APIView):
    """
    List all videos, or create a new video.
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'video_compress/add_video.html'

    #set a flag to keep track if form is submitted, show a success message
    video_successfully_uploaded = None

    def get(self, request, format=None):
        print("inside GET request")
        videos = Video.objects.all()
        form = VideoForm()
        serializer = VideoSerializer(videos, many=True)
        return Response({'serializer': serializer.data, 'form': form})

    def post(self, request, format=None):
        print("inside post request")
        #import pdb; pdb.set_trace()
        data = request.data

        #out time of request
        data['time'] = self.time = datetime.now()

        serializer = VideoSerializer(data=data)
        print data['video']
        # print serializer

        if serializer.is_valid():
            print("form is super valid :)")
            # read width, height and audio_frequency from user
            width = data['desired_width']
            height = data['desired_height']
            audio_frequency = data['desired_audio_frequency']
            print(width, height, int(audio_frequency))

            # get the uploaded video
            uploaded_video = data['video']
            #calculate path of folder where video is saved
            path = settings.BASE_DIR + '/compressing/'

            # storing video on local disk before sending it to s3
            with open(path+uploaded_video.name, 'wb+') as destination:
                destination.write(uploaded_video.read())

            # save video on s3
            print("Now actually saving data.")
            serialized_data = serializer.save()
            print 'this is serialized data', type(serialized_data)

            # make the success message flag True
            video_successfully_uploaded = True
            print 'video_successfully_uploaded', video_successfully_uploaded

            # get the primary key of newly saved object so that the video_compression task can update same
            # serialized_data = serialized_data.id
            object_id = serialized_data.id

            # start a task to compress video
            video_compress_task.delay(uploaded_video.name, object_id, width, height, audio_frequency)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        print ':::DDDDDDDDDDDDDDDDDDDDDDDDDDDDDD'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
