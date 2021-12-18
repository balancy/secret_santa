from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.LoginUserView.as_view(), name='login'),
    path('logout', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.register_user, name='register'),
    path('register/<str:hashed_pk>/', views.register_user, name='register'),
    path('profile', views.view_profile, name='profile'),
    path('santacard', views.update_santa_card, name='santacard'),
    path('create_game', views.create_game, name='create_game'),
    path('update_game/<int:pk>', views.update_game, name='update_game'),
    path('update_user', views.update_user, name='update_user'),
    path(
        'remove_santa_from_game/<int:game_pk>/<int:santa_pk>/',
        views.remove_santa_from_game,
        name='remove_santa_from_game',
    ),
    path(
        'remove_exclusion_from_game/<int:game_pk>/<int:exclusion_pk>/',
        views.remove_exclusion_from_game,
        name='remove_exclusion_from_game',
    ),
    path('greeting/', views.greeting_page, name='greeting_page'),
    path('congrat_page/', views.congrat_page, name='congrat_page'),
]
