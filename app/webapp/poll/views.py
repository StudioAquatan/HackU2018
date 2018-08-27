from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
import django_filters
from django.db.models.functions import Now
from django.db.models import Max

from django.utils import timezone
from datetime import timedelta

from .models import VoteTable, RoomTable
from .serializer import VoteSerializer, RoomSerializer

import re


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
    # 部屋をしぼる機能はまだない

    max_slide = VoteTable.objects.all().aggregate(Max('slide_no'))['slide_no__max']
    slide_list = []  # slide_1, slide_2, ... slide_n
    time_list = []   # 時間(x軸)
    data1_list = []  # わかる
    data2_list = []  # しってる
    data3_list = []  # わからん
    regex = r'\d\d:\d\d:\d\d'

    for i in range(1, int(max_slide) + 1):
        # スライドタイトル(slide_n)のリストに追加
        slide_list.append('slide_' + str(i))

        # スライドごとのデータを作成
        times = ['x']
        data1s = ['分かった']
        data2s = ['もう知ってる']
        data3s = ['分からない']
        data1sum = 0
        data2sum = 0
        data3sum = 0
        votes = VoteTable.objects.filter(slide_no__exact=i).order_by('vote_time')
        for vote in votes:
            time_str = re.search(regex, str(timezone.localtime(vote.vote_time))).group()
            times.append(time_str)
            if vote.vote_type == 1:
                data1sum += 1
            elif vote.vote_type == 2:
                data2sum += 1
            elif vote.vote_type == 3:
                data3sum += 1
            else:
                pass
            append_data(data1s, data2s, data3s, data1sum, data2sum, data3sum)
        time_list.append(times)
        append_data(data1_list, data2_list, data3_list, data1s, data2s, data3s)

    print(time_list)
    return render(request, template_name, {
        'slide_list': slide_list,  # スライドのタイトル'slide_n'のリスト，要素数はスライドの枚数
        'max_slide': max_slide,  # スライドの枚数
        'time_list': time_list,
        'data1_list': data1_list,
        'data2_list': data2_list,
        'data3_list': data3_list,
    })


def append_data(a, b, c, x, y, z):
    a.append(x)
    b.append(y)
    c.append(z)


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
