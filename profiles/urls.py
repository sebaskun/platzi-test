from django.urls import path

from . import views

urlpatterns = [

    path(
        route='signup/',
        view=views.SignupUserView.as_view(),
        name='signup'),

    path(
        route='login/',
        view=views.LoginUserView.as_view(),
        name='login'),
        
    path(
        route='logout/',
        view=views.LogoutUserView.as_view(),
        name='logout'),
]
