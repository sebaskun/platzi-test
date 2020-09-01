from django.urls import path

from . import views

urlpatterns = [
    path(
        route='',
        view=views.VideoListView.as_view(),
        name='list'),

    path(
        route='popular/',
        view=views.Top5VideoListView.as_view(),
        name='popular'),

    path(
        route='history/',
        view=views.VideoHistory.as_view(),
        name='history'),

    path(
        route='<slug:slug>/',
        view=views.VideoDetailView.as_view(),
        name='detail'),

    path(
        route='<str:youtube_id>/like',
        view=views.like_video,
        name='likes_video'
    ),

    path(
        route='<str:youtube_id>/dislike',
        view=views.dislike_video,
        name='dislikes_video'
    ),

    path(
        route='<str:youtube_id>/comment',
        view=views.comment_video,
        name='comment_video'
    ),
]
