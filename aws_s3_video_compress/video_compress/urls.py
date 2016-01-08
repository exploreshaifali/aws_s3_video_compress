from django.conf.urls import url

from video_compress import views

urlpatterns = [
    # url('', 'video_compress.views.add_video', name='add_video'),
    url('', views.VideoList.as_view(), name='add_video'),
]

