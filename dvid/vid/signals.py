from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Video
from .tasks import video_encode

@receiver(post_save,sender=Video)
def video_signal(sender, instance, created, *args, **kwargs):
    if instance and created:
        video_encode.delay(5,instance.id)
    else:
        print("Updated")