from django.shortcuts import render
from video_compress.forms import VideoForm
from video_compress.models import Video
from video_compress.tasks import video_compress_task, hello_task

# Create your views here.

def add_video(request):
    #set a flag to keep track is form is submitted, to show a success message
    video_successfully_uploaded = None
    # if request is post, its form submission time :)
    if request.method == "POST":
        print("inside post request")
        form = VideoForm(request.POST, request.FILES)
        # check, form will be saved only if it is valid
        if form.is_valid():
            print("form is super valid :)")

            # read width, height and audio_frequency from user
            width = request.POST['desired_width']
            height = request.POST['desired_height']
            audio_frequency = request.POST['desired_audio_frequency']
            print(width, height, int(audio_frequency))

            # get the uploaded video
            uploaded_video = request.FILES['video']
            # storing video on local disk before sending it to s3
            with open('./compressing/'+uploaded_video.name, 'wb+') as destination:
                destination.write(uploaded_video.read())

            # save video on s3
            print("Now actually saving data.")
            form_data = form.save()
            #make the success message True
            video_successfully_uploaded = True
            # gave the primary key of newly saved object so that the video_compression task can update same
            object_id = form_data.id
            print(uploaded_video, object_id, width, height, audio_frequency)

            # start a task to compress video
            video_compress_task.delay(uploaded_video.name, object_id, width, height, audio_frequency)

        else:
            print("form is not valid")
    else:
        print("its get request")
        form = VideoForm()
    # get list of all videos saved in s3
    all_videos = Video.objects.order_by('-id').exclude(compressed_video='')
    return render(request, 'video_compress/add_video.html', {'form': form, 'video_list': all_videos,
                  'video_successfully_uploaded': video_successfully_uploaded})
