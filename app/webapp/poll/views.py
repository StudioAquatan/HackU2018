from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
import django_filters
from django.db.models.functions import Now

from django.utils import timezone
from datetime import timedelta

from .models import VoteTable, RoomTable
from .serializer import VoteSerializer, RoomSerializer


def index(request):
    template_name = 'poll/index.html'

    return render(request, template_name)
    # return HttpResponse("Hello, world. You're at the polls index.")


def listener(request):
    template_name = 'poll/listener.html'

    return render(request, template_name)


def speaker(request):
    template_name = 'poll/speaker.html'

    return render(request, template_name)


def speaker_res(request):
    template_name = 'poll/speaker_res.html'

    return render(request, template_name, {
        'slidenum': ['slide1', 'slide2'],  # テスト用データ
        'test_number': 100  # テスト用データ
    })


class VoteViewSet(viewsets.ModelViewSet):
    """
    現在の時間から過去30秒の票だけ表示する
    """
    late_limit_sec = 30
    queryset = VoteTable.objects.filter(vote_time__gte=timezone.now() - timedelta(seconds=late_limit_sec))
    # queryset = VoteTable.objects.filter(vote_time__gte=timezone.now() - timedelta(hours=10))
    serializer_class = VoteSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    現在いる部屋の情報を返す
    （なお現在は部屋をつくる機能がないため常に部屋数が1つであることから全ての部屋情報を返すコードになっている）
    """
    queryset = RoomTable.objects.all()
    serializer_class = RoomSerializer
