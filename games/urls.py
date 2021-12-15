from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path(
        'login',
        views.LoginUserView.as_view(),
        name='login',
    ),
    path('profile', views.view_profile, name='profile'),
    path('santacard/', views.create_santa_card, name='santacard')
]
