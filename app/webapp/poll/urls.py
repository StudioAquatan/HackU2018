from django.urls import path
from rest_framework import routers

from .views import VoteViewSet, RoomViewSet
from . import views

app_name = 'poll'

router = routers.DefaultRouter()
router.register(r'votes', VoteViewSet)
router.register(r'room-people', RoomViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('listener/', views.listener, name='listener'),
    path('speaker/', views.speaker, name='speaker'),
    path('speaker/res', views.speaker_res, name='speaker_res'),
]
