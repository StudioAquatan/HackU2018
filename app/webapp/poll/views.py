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
import datetime

from .listener_button import button1, button2, button3, comment_submit


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
        input_comment = request.POST.get('input_comment')
        if 'button_1' in request.POST:
            # ボタン1がクリックされた場合の処理
            button1()
        elif 'button_2' in request.POST:
            # ボタン2がクリックされた場合の処理
            button2()
        elif 'button_3' in request.POST:
            # ボタン2がクリックされた場合の処理
            button3()
        elif 'button_submit' in request.POST:
            comment_submit(input_comment)

    return render(request, template_name)


def speaker_start(request):
    template_name = 'poll/speaker-start.html'

    return render(request, template_name)


def speaker(request):
    template_name = 'poll/speaker.html'

    return render(request, template_name)


def speaker_res(request):
    template_name = 'poll/speaker_res.html'

    # --------------------グラフ機能--------------------
    # スライドの枚数，最後に終わったスライドのslide_noを見ている
    slide_num = SlideTable.objects.all().order_by('-end_time').first().slide_no
    # TODO: 部屋でフィルタをかける

    slide_list = []  # slide_1, slide_2, ... slide_n
    time_list = []  # 時間(x軸)
    data1_list = []  # わかる
    data2_list = []  # しってる
    data3_list = []  # わからん
    regex_time = r'\d\d:\d\d:\d\d'
    regex_date_time = r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d'
    time_divide = 10  # グラフの集計をする時の区切りの秒数.例えばtime_divide=10の場合，グラフは最低10秒の間隔ができる．

    for i in range(1, int(slide_num) + 1):
        # スライドタイトル(slide_i)のリストに追加
        slide_list.append('slide_' + str(i))

        # スライドごとのデータを作成
        slide_start_time = SlideTable.objects.filter(slide_no__exact=i).order_by('-end_time').first().start_time
        slide_st_time = re.search(regex_time, str(timezone.localtime(slide_start_time))).group()
        slide_end_time = SlideTable.objects.filter(slide_no__exact=i).order_by('-end_time').first().end_time
        slide_ed_time = re.search(regex_time, str(timezone.localtime(slide_end_time))).group()
        times = ['x', slide_st_time]
        data1s = ['分かった', 0]  # スライド開始時はすべて0票
        data2s = ['もう知ってる', 0]
        data3s = ['分からない', 0]
        data1sum = 0
        data2sum = 0
        data3sum = 0
        time_temp = slide_start_time
        plus_time_div = time_temp + datetime.timedelta(seconds=time_divide)

        # time_divideごとのデータを作成する
        while plus_time_div < slide_end_time:
            # slide_no == i && time_temp <= vote_time < plus_time_div
            votes = VoteTable.objects\
                .filter(slide_id__slide_no__exact=i, vote_time__gte=time_temp, vote_time__lt=plus_time_div)\
                .order_by('vote_time')
            for vote in votes:
                if vote.vote_type == 1:
                    data1sum += 1
                elif vote.vote_type == 2:
                    data2sum += 1
                elif vote.vote_type == 3:
                    data3sum += 1
                else:
                    pass
            times.append(re.search(regex_time, str(timezone.localtime(plus_time_div))).group())
            append_data(data1s, data2s, data3s, data1sum, data2sum, data3sum)
            data1sum = 0
            data2sum = 0
            data3sum = 0
            time_temp = plus_time_div
            plus_time_div += datetime.timedelta(seconds=time_divide)

        # スライド終了
        votes = VoteTable.objects \
            .filter(slide_id__slide_no__exact=i, vote_time__gte=time_temp, vote_time__lte=slide_end_time) \
            .order_by('vote_time')
        for vote in votes:
            if vote.vote_type == 1:
                data1sum += 1
            elif vote.vote_type == 2:
                data2sum += 1
            elif vote.vote_type == 3:
                data3sum += 1
            else:
                pass
        times.append(slide_ed_time)
        append_data(data1s, data2s, data3s, data1sum, data2sum, data3sum)
        # スライドのデータを追加
        time_list.append(times)
        append_data(data1_list, data2_list, data3_list, data1s, data2s, data3s)

    # --------------------コメント機能--------------------
    # 部屋関係なしに全データ取得
    speak_start_time = SlideTable.objects.filter(slide_no__exact=1).order_by('-start_time').first().start_time
    comments = CommentTable.objects.filter(comment_time__gte=speak_start_time).order_by('comment_time')
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
    # デモ用(過去10秒の票を持ってくる)
    # late_limit_sec = 10
    # 展示用(過去60秒の票を持ってくる)
    # late_limit_sec 60
    # 過去late_limit[sec]の票を持ってくる
    # queryset = VoteTable.objects.filter(slide_no=current_slide.slide_no,
    #                                     vote_time__gte=timezone.now() - timedelta(seconds=late_limit_sec))
    # ↓時間にかかわらず全てとってくる
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
