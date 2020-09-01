from django.db import models
from django.contrib.auth.models import User
from videos.models import Video
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    history = models.ManyToManyField(Video)

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserHistory.objects.create(user=instance)
    else:
        try:
            temp = UserHistory.objects.get(user=instance)
        except:
            UserHistory.objects.create(user=instance)
            
