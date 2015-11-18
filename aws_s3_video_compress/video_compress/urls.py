from django.conf.urls import url

urlpatterns = [
    url('', 'video_compress.views.add_video', name='add_video'),
]
