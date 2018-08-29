from django.urls import path
from rest_framework import routers

from .views import VoteViewSet, RoomViewSet,CommentViewSet
from . import views

app_name = 'poll'

router = routers.DefaultRouter()
router.register(r'votes', VoteViewSet)
router.register(r'room-people', RoomViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:roomID>/listener/', views.listener, name='listener'),
    path('<int:roomID>/speaker-start/', views.speaker_start, name='speaker_start'),
    path('<int:roomID>/speaker/', views.speaker, name='speaker'),
    path('<int:roomID>/speaker/res', views.speaker_res, name='speaker_res'),
    path('<int:roomID>/speaker/change-status', views.change_status, name='change-status'),
]
