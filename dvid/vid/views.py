from django.shortcuts import render,get_object_or_404
from vid.models import Video
from django.http import FileResponse, HttpResponse
import os
from django.urls import reverse

# Create your views here.
def serve_hls_playlist(request, video_id):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_playlist_path = video.hls
        
        with open(hls_playlist_path, 'r') as m3u8_file:
            m3u8_content = m3u8_file.read()
        
        base_url = request.build_absolute_uri('/') 

        serve_hls_segment_url = base_url +"serve_hls_segment/" +str(video_id)
        m3u8_content = m3u8_content.replace('{{ dynamic_path }}', serve_hls_segment_url)

        return HttpResponse(m3u8_content, content_type='application/vnd.apple.mpegurl')
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS playlist not found", status=404)


def serve_hls_segment(request, video_id, segment_name):
    try:
        video = get_object_or_404(Video, pk=video_id)
        hls_directory = os.path.join(os.path.dirname(video.video.path), 'hls_output')
        print("HLS DIRECTORY",hls_directory)
        segment_path = os.path.join(hls_directory, segment_name)
        # Serve the HLS segment as a binary file response
        return FileResponse(open(segment_path, 'rb'))
    except (Video.DoesNotExist, FileNotFoundError):
        return HttpResponse("Video or HLS segment not found", status=404)

def all_videos(request):
    videos = Video.objects.filter(status='Completed')

    context = {
        "videos":videos
    }

    return render(request, 'all_videos.html', context)


def hls_video_player(request, video_id):
    video = Video.objects.filter(slug=video_id).first()

    context = {
        'hls_url': reverse(serve_hls_playlist, args=[video.id]),
        'video': video,
    }

    print(context)
    return render(request, 'video_player.html', context)


    




