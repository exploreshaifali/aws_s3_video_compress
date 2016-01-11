from django.views.generic.base import TemplateView

from video_compress.forms import VideoForm
from video_compress.models import Video


class HomePageView(TemplateView):

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        videos = Video.objects.order_by('-id').exclude(compressed_video='')
        form = VideoForm()
        context['form'] = form
        context['videos'] =  videos
        return context
