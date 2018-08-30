from django.urls import path
from rest_framework import routers

from .views import VoteViewSet, RoomViewSet, CommentViewSet,SlideViewSet
from . import views

app_name = 'poll'

router = routers.DefaultRouter()
router.register(r'votes', VoteViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'slides', SlideViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:room_id>/listener_a/', views.listener_a, name='listener_a'),
    path('<int:room_id>/listener_b/', views.listener_b, name='listener_b'),
    path('<int:room_id>/speaker-start/', views.speaker_start, name='speaker_start'),
    path('<int:room_id>/speaker/', views.speaker, name='speaker'),
    path('<int:room_id>/speaker/res', views.speaker_res, name='speaker_res'),
    path('<int:room_id>/speaker/change-status', views.change_status, name='change-status'),
]
