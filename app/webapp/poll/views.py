from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets
from django.urls import reverse
from django.db.models import Max
from django.utils import timezone
from datetime import timedelta
from .models import VoteTable, RoomTable, CommentTable, SlideTable
from .serializer import VoteSerializer, RoomSerializer, CommentSerializer, SlideSerializer
import re
import datetime
from .listener_button import button1, button2, button3, comment_submit
from .forms import RoomForm


def index(request):
    room = RoomTable()
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            room = form.save(commit=False)
            input_name = room.room_name
            if request.POST['action'] == 'make_room':
                # 同じ名前の部屋がすでにあればエラーメッセージを出させる
                if RoomTable.objects.filter(room_name__exact=input_name).exists():
                    return render(request, 'poll/index.html', {
                        'form': form,
                        'error_message': '"' + input_name + '"はすでに存在します．'
                    })
                else:
                    room.save()
                    return HttpResponseRedirect(reverse('poll:speaker_start', args=(room.id,)))
            elif request.POST['action'] == 'view_results':
                view = RoomTable.objects.filter(room_name__exact=input_name).first()
                if view is None:
                    return render(request, 'poll/index.html', {
                        'form': form,
                        'error_message': '"' + input_name + '"は存在しません．'
                    })
                else:
                    return HttpResponseRedirect(reverse('poll:speaker_res', args=(view.id,)))
            elif request.POST['action'] == 'join_room':
                join = RoomTable.objects.filter(room_name__exact=input_name).first()
                if join is None:
                    return render(request, 'poll/index.html', {
                        'form': form,
                        'error_message': '"' + input_name + '"は存在しません．'
                    })
                else:
                    return HttpResponseRedirect(reverse('poll:listener_a', args=(join.id,)))
            else:
                pass
    else:
        form = RoomForm(instance=room)

    return render(request, 'poll/index.html', {'form': form})


# 一回目のリスナーページ読み込み
def listener_a(request, room_id):
    template_name = 'poll/listener_a.html'

    if request.method == 'POST':
        input_comment = request.POST.get('input_comment')
        if 'button_1' in request.POST:
            # ボタン1がクリックされた場合の処理
            button1(room_id)
            template_name = 'poll/listener_b.html'
        elif 'button_2' in request.POST:
            # ボタン2がクリックされた場合の処理
            button2(room_id)
            template_name = 'poll/listener_b.html'
        elif 'button_3' in request.POST:
            # ボタン3がクリックされた場合の処理
            button3(room_id)
            template_name = 'poll/listener_b.html'
        elif 'button_submit' in request.POST:
            comment_submit(input_comment, room_id)

    return render(request, template_name, {'room_id': room_id})


# 二回目以降のリスナーページ読み込み
def listener_b(request, room_id):
    template_name = 'poll/listener_b.html'

    if request.method == 'POST':
        input_comment = request.POST.get('input_comment')
        if 'button_1' in request.POST:
            # ボタン1がクリックされた場合の処理
            button1(room_id)
        elif 'button_2' in request.POST:
            # ボタン2がクリックされた場合の処理
            button2(room_id)
        elif 'button_3' in request.POST:
            # ボタン3がクリックされた場合の処理
            button3(room_id)
            template_name = 'poll/listener_b.html'
        elif 'button_submit' in request.POST:
            comment_submit(input_comment, room_id)

    return render(request, template_name, {'room_id': room_id})


def listener_b(request, room_id):
    template_name = 'poll/listener_b.html'

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

    return render(request, template_name, {'room_id': room_id})


def speaker_start(request, room_id):
    template_name = 'poll/speaker-start.html'

    return render(request, template_name, {'room_id': room_id})


def speaker(request, room_id):
    template_name = 'poll/speaker.html'

    return render(request, template_name, {'room_id': room_id})


def speaker_res(request, room_id):
    template_name = 'poll/speaker_res.html'

    # --------------------グラフ機能--------------------
    # スライドの枚数，room_idの中で一番大きいslide_no
    slide_num = SlideTable.objects.filter(room_id_id__exact=room_id).aggregate(Max('slide_no'))['slide_no__max']

    slide_list = []  # slide_1, slide_2, ... slide_n
    time_list = []  # 時間(x軸)
    data1_list = []  # わかる
    data2_list = []  # しってる
    data3_list = []  # わからん
    regex_time = r'\d\d-\d\d \d\d:\d\d:\d\d'
    regex_date_time = r'\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d'
    time_divide = 10  # グラフの集計をする時の区切りの秒数.例えばtime_divide=10の場合，グラフは最低10秒の間隔ができる．

    for i in range(1, int(slide_num) + 1):
        # スライドタイトル(slide_i)のリストに追加
        slide_list.append('slide_' + str(i))

        # スライドごとのデータを作成
        slide_start_time = SlideTable.objects.filter(room_id_id__exact=room_id, slide_no__exact=i).first().start_time
        slide_st_time = re.search(regex_time, str(timezone.localtime(slide_start_time))).group()
        slide_end_time = SlideTable.objects.filter(room_id_id__exact=room_id, slide_no__exact=i).first().end_time
        if slide_end_time is None:  # 講義中にHOMEに戻りView resultsを押すと起こる
            slide_end_time = timezone.now()
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
            # room_id_id == room_id && slide_no == i && time_temp <= vote_time < plus_time_div
            votes = VoteTable.objects \
                .filter(slide_id__room_id_id__exact=room_id, slide_id__slide_no__exact=i,
                        vote_time__gte=time_temp, vote_time__lt=plus_time_div) \
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
            .filter(slide_id__room_id_id__exact=room_id, slide_id__slide_no__exact=i,
                    vote_time__gte=time_temp, vote_time__lte=slide_end_time) \
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
    # room_idの部屋の全データ取得
    comments = CommentTable.objects.filter(slide_id__room_id_id__exact=room_id).order_by('comment_time')
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


def change_status(request, room_id):
    room_info = RoomTable.objects.filter(id=room_id).first()

    if request.POST['action'] == 'start-lec':
        SlideTable.objects.create(slide_no=1, start_time=timezone.now(), room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker', args=(room_id,)))

    elif request.POST['action'] == 'next-slide':
        current_slide = SlideTable.objects.filter(room_id=room_info).order_by('start_time').last()
        current_slide.end_time = timezone.now()
        current_slide.save()
        SlideTable.objects.create(slide_no=current_slide.slide_no + 1, start_time=timezone.now(), room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker', args=(room_id,)))

    elif request.POST['action'] == 'fin-lec':
        current_slide = SlideTable.objects.filter(room_id=room_info).order_by('start_time').last()
        current_slide.end_time = timezone.now()
        current_slide.save()
        return HttpResponseRedirect(reverse('poll:speaker_res', args=(room_id,)))


class VoteViewSet(viewsets.ModelViewSet):
    """
    現在発表中のスライド(startが最も遅いslide)に対する現在の時間から過去30秒の票だけ返す
    部屋とスライドの何枚目かを指定する場合は
    /api/votes/?slide_id__slide_no=<何枚目か>&slide_id__room_id__id=<欲しい部屋のpk>
    """
    queryset = VoteTable.objects.all()
    serializer_class = VoteSerializer
    filter_fields = ('slide_id__slide_no', 'slide_id__room_id__id',)

    def get_queryset(self):
        """querysetを取得する関数をオーバーライド"""
        queryset = super(VoteViewSet, self).get_queryset()
        return queryset.filter(vote_time__gte=timezone.now() - timedelta(seconds=10))


class RoomViewSet(viewsets.ModelViewSet):
    """
    存在する部屋の情報全て返す
    部屋を指定する場合は  /api/rooms/?id=<欲しい部屋のpk>
    """
    queryset = RoomTable.objects.all()
    serializer_class = RoomSerializer
    filter_fields = ('id',)


class CommentViewSet(viewsets.ModelViewSet):
    """
    現在発表中のスライド(startが最も遅いslide)に対するコメントを返す
    部屋とスライドの何枚目かを指定する場合は
    /api/comments/?slide_id__slide_no=<何枚目か>&slide_id__room_id__id=<欲しい部屋のpk>
    """
    queryset = CommentTable.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('slide_id__slide_no', 'slide_id__room_id__id',)


class SlideViewSet(viewsets.ModelViewSet):
    """
    存在するスライドの情報全て返す
    部屋を指定する場合は  /api/slides/?room_id__id=<欲しい部屋のpk>
    """
    queryset = SlideTable.objects.all()
    serializer_class = SlideSerializer
    filter_fields = ('room_id__id',)
