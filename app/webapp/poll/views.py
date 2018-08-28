from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
import django_filters
from django.urls import reverse
from django.db.models.functions import Now
from django.db.models import Max

from django.utils import timezone
from datetime import timedelta

from .models import VoteTable, RoomTable, CommentTable, SlideTable
from .serializer import VoteSerializer, RoomSerializer, CommentSerializer

import re

from .listener_button import button1, button2, button3


def index(request):
    template_name = 'poll/index.html'

    if request.method == 'GET':
        if 'make_room' in request.GET:
            # ボタン1がクリックされた場合の処理
            button1()
            template_name = 'poll/listener.html'
        elif 'join_room' in request.GET:
            # ボタン2がクリックされた場合の処理
            button2()
            template_name = 'poll/speaker-start.html'

    return render(request, template_name)
    # return HttpResponse("Hello, world. You're at the polls index.")


def listener(request):
    template_name = 'poll/listener.html'

    if request.method == 'POST':
        if 'button_1' in request.POST:
            # ボタン1がクリックされた場合の処理
            button1()
        elif 'button_2' in request.POST:
            # ボタン2がクリックされた場合の処理
            button2()
        elif 'button_3' in request.POST:
            # ボタン2がクリックされた場合の処理
            button3()

    return render(request, template_name)


def speaker_start(request):
    template_name = 'poll/speaker-start.html'

    return render(request, template_name)


def speaker(request):
    template_name = 'poll/speaker.html'

    return render(request, template_name)


def speaker_res(request):
    template_name = 'poll/speaker_res.html'

    # グラフ機能
    # 部屋関係なしに全部のデータをとる
    # スライドの枚数
    # TODO: 部屋でフィルタをかける
    slide_num = SlideTable.objects.all().aggregate(Max('slide_no'))['slide_no__max']

    slide_list = []  # slide_1, slide_2, ... slide_n
    time_list = []  # 時間(x軸)
    data1_list = []  # わかる
    data2_list = []  # しってる
    data3_list = []  # わからん
    regex_time = r'\d\d:\d\d:\d\d'
    regex_date_time = r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d'

    for i in range(1, int(slide_num) + 1):
        # スライドタイトル(slide_i)のリストに追加
        slide_list.append('slide_' + str(i))

        # スライドごとのデータを作成
        slide_start_time = SlideTable.objects.filter(slide_no__exact=i)[0].start_time
        slide_start_time = re.search(regex_time, str(timezone.localtime(slide_start_time))).group()
        times = ['x', slide_start_time]
        data1s = ['分かった', 0]  # スライド開始時はすべて0票
        data2s = ['もう知ってる', 0]
        data3s = ['分からない', 0]
        # times = ['x']
        # data1s = ['分かった']
        # data2s = ['もう知ってる']
        # data3s = ['分からない']
        data1sum = 0
        data2sum = 0
        data3sum = 0
        # i番目のスライドの，vote_timeでソートされたvoteオブジェクトのリストを作成
        votes = VoteTable.objects.filter(slide_id__slide_no__exact=i).order_by('vote_time')
        for vote in votes:
            time_str = re.search(regex_time, str(timezone.localtime(vote.vote_time))).group()
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
        # スライド終了
        slide_end_time = SlideTable.objects.filter(slide_no__exact=i)[0].end_time
        slide_end_time = re.search(regex_time, str(timezone.localtime(slide_end_time))).group()
        times.append(slide_end_time)
        append_data(data1s, data2s, data3s, data1sum, data2sum, data3sum)
        # スライドのデータを追加
        time_list.append(times)
        append_data(data1_list, data2_list, data3_list, data1s, data2s, data3s)

    # コメント機能
    # 部屋関係なしに全データ取得
    comments = CommentTable.objects.all().order_by('comment_time')
    comment_dic_list = []
    for comment in comments:
        dic = dict()
        dic['slide'] = comment.slide_id.slide_no
        date_time_str = re.search(regex_date_time, str(timezone.localtime(comment.comment_time))).group()
        date_time_str = date_time_str.replace('-', '/')
        dic['time'] = date_time_str
        dic['text'] = comment.comment_text
        comment_dic_list.append(dic)

    return render(request, template_name, {
        'slide_list': slide_list,  # スライドのタイトル'slide_n'のリスト，要素数はスライドの枚数
        'slide_num': slide_num,  # スライドの枚数
        'time_list': time_list,
        'data1_list': data1_list,
        'data2_list': data2_list,
        'data3_list': data3_list,
        'comment_dic_list': comment_dic_list
    })


def append_data(a, b, c, x, y, z):
    a.append(x)
    b.append(y)
    c.append(z)


def change_status(request):
    # TODO 任意のroom_idの取得
    room_info = RoomTable.objects.first()

    if request.POST['action'] == 'start-lec':
        SlideTable.objects.create(slide_no=1, start_time=timezone.now(), room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker'))

    elif request.POST['action'] == 'next-slide':
        current_slide = SlideTable.objects.order_by('start_time').last()
        current_slide.end_time = timezone.now()
        current_slide.save()
        SlideTable.objects.create(slide_no=current_slide.slide_no + 1, start_time=timezone.now(), room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker'))

    elif request.POST['action'] == 'fin-lec':
        current_slide = SlideTable.objects.order_by('start_time').last()
        current_slide.end_time = timezone.now()
        current_slide.save()
        return HttpResponseRedirect(reverse('poll:speaker_res'))


class VoteViewSet(viewsets.ModelViewSet):
    """
    現在発表中のスライド(startが最も遅いslide)に対する現在の時間から過去30秒の票だけ返す
    現状部屋の区別はつけていない
    （将来的に部屋に合わせた票の取得をしたい）
    """
    current_slide = SlideTable.objects.order_by('start_time').last()
    late_limit_sec = 30
    # queryset = VoteTable.objects.filter(slide_no=current_slide.slide_no,
    #                                     vote_time__gte=timezone.now() - timedelta(seconds=late_limit_sec))
    # ↓時間にかかわらずとってくる
    queryset = VoteTable.objects.filter(slide_id=current_slide)
    serializer_class = VoteSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    現在いる部屋の情報を返す
    （なお現在は部屋をつくる機能がないため常に部屋数が1つであることから全ての部屋情報を返すコードになっている）
    """
    queryset = RoomTable.objects.all()
    serializer_class = RoomSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """
    現在発表中のスライド(startが最も遅いslide)に対するコメントを返す
    現状部屋の区別はつけていない
    （将来的に部屋に合わせたコメント取得をしたい）
    """
    current_slide = SlideTable.objects.order_by('start_time').last()
    queryset = CommentTable.objects.filter(slide_id=current_slide)
    serializer_class = CommentSerializer
