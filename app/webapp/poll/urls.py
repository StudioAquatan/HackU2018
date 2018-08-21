from django.urls import path

from . import views

app_name = 'poll'
urlpatterns = [
    path('', views.index, name='index'),
    path('listener/', views.listener, name='listener'),
]
