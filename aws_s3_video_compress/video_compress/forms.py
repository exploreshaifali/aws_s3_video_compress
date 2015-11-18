from django import forms

from video_compress.models import Video


class VideoForm(forms.ModelForm):
    desired_width = forms.IntegerField(min_value=1)
    desired_height = forms.IntegerField(min_value=1)
    desired_audio_frequency = forms.IntegerField(min_value=1)

    class Meta:
        model = Video
        fields = ('title', 'video',)
