from django.urls import path
from .views import all_videos,hls_video_player,serve_hls_playlist,serve_hls_segment

urlpatterns = [
    path('', all_videos, name='all_videos'),
    path('<slug:video_id>/',hls_video_player, name='hls_video_player'),
    path('serve_hls_playlist/<int:video_id>/',serve_hls_playlist, name='serve_hls_playlist'),
    path('serve_hls_segment/<int:video_id>/<str:segment_name>',serve_hls_segment, name='serve_hls_segment')
    ]