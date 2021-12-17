from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('register/', views.register_user, name='register'),
    path('register/<int:pk>/', views.register_user, name='register'),
    path('profile/', views.view_profile, name='profile'),
    path('santacard/', views.update_santa_card, name='santacard'),
    path('create_game/', views.create_game, name='create_game'),
    path('update_game/<int:pk>/', views.update_game, name='update_game'),
    path(
        'remove_santa_from_game/<int:game_pk>/<int:santa_pk>/',
        views.remove_santa_from_game,
        name='remove_santa_from_game',
    ),
    path('greeting/', views.greeting_page, name='greeting_page'),
]
