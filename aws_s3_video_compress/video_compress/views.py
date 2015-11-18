from django.shortcuts import render
from video_compress.forms import VideoForm
from video_compress.models import Video

# Create your views here.

def add_video(request):
    # if request is post, its form submission time :)
    if request.method == "POST":
        print("inside post request")
        form = VideoForm(request.POST, request.FILES)
        # check, form will be saved only if it is valid
        if form.is_valid():
            print("form is super valid :)")

            # save video on s3
            print("Now actually saving data.")
            form_data = form.save()

        else:
            print("form is not valid")
    else:
        print("its get request")
        form = VideoForm()
    # get list of all videos saved in s3
    all_videos = Video.objects.order_by('-id').exclude(compressed_video='')
    return render(request, 'video_compress/add_video.html', {'form': form, 'video_list': all_videos})
