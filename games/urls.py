from django.urls import path

from games import views

urlpatterns = [
    path('', views.index, name='index'),
]
