from rest_framework import serializers

from video_compress.models import Video

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('id', 'video', 'title', 'time', 'compressed_video')