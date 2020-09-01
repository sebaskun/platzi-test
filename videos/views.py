from django.shortcuts import render, redirect
from django.db.models import Count, F, Case, When, IntegerField
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, View
from django.views.decorators.http import require_http_methods
from django.core import serializers

import datetime
from .models import Video, Comment
from profiles.models import UserHistory

class VideoListView(ListView):
    model=Video
    template_name="videos/list.html"
    paginate_by = 10

class VideoHistory(ListView):
    model=Video
    template_name="videos/list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        history = []
        if not request.user.is_anonymous:
            user = request.user
            history = UserHistory.objects.get(user=user)

        self.object_list = self.get_queryset().filter(pk__in=history.history.all())
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

class Top5VideoListView(ListView):
    model=Video
    template_name="videos/list.html"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset().annotate(
            likes_count=Count('likes')).annotate(
                comments_count=Count('comments')).annotate(
                    dislikes_count=Count('dislikes')).annotate(
                        is_today=Case(When(created_at__gte=datetime.date.today(), then=1), When(created_at__lt=datetime.date.today(), then=0),output_field=IntegerField(),)).annotate(
                            popularity=F('likes_count')*10 + F('comments_count') - F('dislikes_count')*5 + F('is_today')*100).order_by('-popularity')[:5]
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        context = self.get_context_data()
        return self.render_to_response(context)

class VideoDetailView(DetailView):
    model=Video
    template_name="videos/detail.html"
    query_set=Video.objects.all()
    slug_field="slug"
    slug_url_kwarg="slug"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)

        # Add to user history
        if not request.user.is_anonymous:
            try:
                hist = UserHistory.objects.get(user=request.user)
                hist.history.add(self.object)
                hist.save()
            except:
                pass

        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        ContextOfTheView=super().get_context_data(**kwargs)

        video=self.get_object()

        likes=Video.objects.filter(youtube_id=video.youtube_id).aggregate(dislikes_count=Count('dislikes'), likes_count=Count('likes'))

        ContextOfTheView["comments"]=Comment.objects.filter(video=video)
        ContextOfTheView["likes"]=likes
        return ContextOfTheView

    def render_to_response(self, context, **response_kwargs):
        video=self.get_object()
        video.views=video.views + 1
        video.save()
        
        return super().render_to_response(context, **response_kwargs)

@require_http_methods(["POST"])
def comment_video(request, youtube_id):
    print("dislike a video")
    user_logged=request.user
    x=Video.objects.get(youtube_id=youtube_id)
    
    comment_req=request.POST.get("comment")
    
    comment=Comment.objects.create(
        video=x,
        user=user_logged,
        comment=comment_req
    )

    return redirect(reverse_lazy("videos:detail", kwargs={"slug": x.slug}))



@require_http_methods(["POST"])
def like_video(request, youtube_id):
    print("dislike a video")
    user_logged=request.user

    video=Video.objects.filter(youtube_id=youtube_id).first()

    if not video:
        return JsonResponse({'error': 'invalid video id'}, status=400)

    video.likes.add(user_logged)

    video.save()

    data={
        "ok": "Like saved"
    }

    return JsonResponse(data)


@require_http_methods(["POST"])
def dislike_video(request, youtube_id):
    print("dislike a video")
    user_logged=request.user

    video=Video.objects.filter(youtube_id=youtube_id, active=True)[0]
    

    video.dislikes.add(user_logged)

    video.save()
   
    data={
        "ok": "Dislike saved"
    }

    return JsonResponse(data)
