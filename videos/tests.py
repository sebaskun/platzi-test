from django.test import TestCase
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse

from faker import Factory

from .models import Video
from profiles.models import UserHistory

# Create your tests here.

faker = Factory.create()

class VideoTests(TestCase):

    def setUp(self):

        # Create some test users
        test_user = User.objects.create_user(
            username='test_user',
            password='123456')
        test_user_2 = User.objects.create_user(
            username='test_user_2',
            password='123456')
        test_user.save()        
        test_user_2.save()

        # Create the videos for tests
        numberOfVideos = 11
        for video in range(numberOfVideos):
            title = faker.sentence(nb_words=5)
            video = Video.objects.create(
                title = title,
                author = faker.name(),
                thumbnail_url = faker.uri(),
                slug = slugify(title),
                youtube_id=faker.random_int())

    def test_list_videos_url_exists(self):
        resp = self.client.get(reverse('videos:list'))
        self.assertEqual(resp.status_code, 200)

    def test_pagination_is_ten(self):

        resp = self.client.get(reverse('videos:list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 10)

    def test_remain_one_item(self):

        resp = self.client.get(reverse('videos:list')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue(len(resp.context['object_list']) == 1)

    def test_detail_video(self):

        video = Video.objects.first()
        resp = self.client.get(reverse(
            'videos:detail', 
            kwargs={'slug': video.slug}))
        self.assertEqual(resp.status_code, 200)

    def test_increments_views_on_request(self):

        video = Video.objects.first()
        resp = self.client.get(reverse(
            'videos:detail', 
            kwargs={'slug': video.slug}))
        self.assertEqual(resp.status_code, 200)
        video_after_request = Video.objects.filter(pk=video.pk).first()
        self.assertTrue(video.views == (video_after_request.views - 1))

    def test_like_video(self):

        video = Video.objects.first()
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.post(reverse(
            'videos:likes_video', 
            kwargs={'youtube_id': video.youtube_id}))
        self.assertEqual(resp.status_code, 200)

    def test_dislike_video(self):

        video = Video.objects.first()
        login = self.client.login(username='test_user_2', password='123456')
        resp = self.client.post(reverse(
            'videos:dislikes_video', 
            kwargs={'youtube_id': video.youtube_id}))
        self.assertEqual(resp.status_code, 200)

    def test_like_no_existent_video(self):

        random_youtube_id = faker.sentence(nb_words=1)
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.post(reverse(
            'videos:likes_video', 
            kwargs={'youtube_id': random_youtube_id}))
        self.assertEqual(resp.status_code, 400)

    def test_dislike_no_existent_video(self):

        random_youtube_id = faker.sentence(nb_words=1)
        login = self.client.login(username='test_user_2', password='123456')
        resp = self.client.post(reverse(
            'videos:dislikes_video', 
            kwargs={'youtube_id': random_youtube_id}))
        self.assertEqual(resp.status_code, 400)

    def test_popular_videos_url_exists(self):
        resp = self.client.get(reverse('videos:popular'))
        self.assertEqual(resp.status_code, 200)
    
    def test_history_videos_url_exists(self):
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('videos:history'))
        self.assertEqual(resp.status_code, 200)

    def test_history_videos_add_history(self):
        video = Video.objects.first()
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse(
            'videos:detail', 
            kwargs={'slug': video.slug}))
        self.assertTrue(video.userhistory_set.filter(user__username="test_user").exists())


        