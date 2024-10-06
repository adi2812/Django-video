from typing import Any
from django.core.management.base import BaseCommand, CommandError
from vid.models import Video
import os
import subprocess
import json

class Command(BaseCommand):
    help = 'Encode Command'

    def handle(self, *args: Any, **options: Any) -> str | None:
        try:
            obj = Video.objects.filter(status='Pending').first()
            
            if obj:
                print(obj.id)
                obj.status = 'Processing'
                obj.is_running = True
                obj.save()
                input_video_path = obj.video.path

                op_directory = os.path.join(os.path.dirname(input_video_path), "hls_output")
                print(op_directory)
                os.makedirs(op_directory, exist_ok=True)
                op_filename = os.path.splitext(os.path.basename(input_video_path))[0] + '_hls.m3u8'
                op_hls_path = os.path.join(op_directory,op_filename)
                op_thumbnail_path = os.path.join(op_directory,os.path.splitext(os.path.basename(input_video_path))[0]+'_thumbnail.jpg')

                ## Getting duration
                command_duration = [
                    'ffprobe',
                    '-v',
                    'quiet',
                    '-print_format',
                    'json',
                    '-show_streams',
                    input_video_path
                ]

                dur_res = subprocess.run(command_duration,shell=False,check=True,stdout=subprocess.PIPE)
                op_json = json.loads(dur_res.stdout)
                video_length = None

                
                for stream in op_json['streams']:
                    if stream['codec_type'] == 'video':
                        video_length = stream['duration']
                        break
                

                ## Creating Thumbnail file
                thumb_args = [
                              "ffmpeg",
                              "-i",
                              input_video_path,
                              "-ss",
                              "2",
                              "-vframes",
                              "1",
                              "-q:v",
                              "2",
                              "-y",
                              op_thumbnail_path
                              ]
                
                subprocess.run(thumb_args,check=True)

                ## Creating ts file
                pro_args = [
                    "ffmpeg",
                    "-i",
                    input_video_path,
                    "-c:v",
                    "h264",
                    "-c:a",
                    "aac",
                    "-hls_time",
                    "5",
                    "-hls_list_size",
                    "0",
                    "-hls_base_url",
                    "{{ dynamic_path }}/",
                    "-movflags",
                    "+faststart",
                    "-y",
                    op_hls_path
                ]

                subprocess.run(pro_args,check=True)

                obj.hls = op_hls_path
                obj.duration = video_length
                obj.thumbnail = op_thumbnail_path
                obj.status = "Completed"
                obj.is_running = False
                obj.save()
                
        except Exception as e:
            print("ERROR",e)

