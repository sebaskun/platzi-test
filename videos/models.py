from django.db import models

from django.contrib.auth.models import User
import datetime

# Create your models here.

class Video(models.Model):
    
    title = models.CharField(
        max_length=256, 
        null=False
    )

    views = models.IntegerField(null=False, default=0)

    author = models.CharField(max_length=200)

    youtube_id = models.CharField(max_length=50, null=False)

    thumbnail_url = models.URLField(max_length=200)

    slug = models.SlugField(max_length=200,unique=True)

    likes = models.ManyToManyField(User)

    dislikes = models.ManyToManyField(
        User, 
        related_name='dislike_videos'
    )

    created_at = models.DateField(default=datetime.date.today)

    comments = models.ManyToManyField(
        User, 
        through='Comment',
        related_name='comments_videos'
    )

    active = models.BooleanField(default=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)

class Comment(models.Model):

    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    comment = models.CharField(max_length=300, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
