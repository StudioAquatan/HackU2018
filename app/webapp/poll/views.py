from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, filters
import django_filters
from django.urls import reverse
from django.db.models.functions import Now

from django.utils import timezone
from datetime import timedelta

from .models import VoteTable, RoomTable, CommentTable
from .serializer import VoteSerializer, RoomSerializer, CommentSerializer


def index(request):
    template_name = 'poll/index.html'

    return render(request, template_name)
    # return HttpResponse("Hello, world. You're at the polls index.")


def listener(request):
    template_name = 'poll/listener.html'

    return render(request, template_name)


def speaker_start(request):
    template_name = 'poll/speaker-start.html'

    return render(request, template_name)


def speaker(request):
    template_name = 'poll/speaker.html'

    # understand_vote = Vote.objects.filter(votetype=0)
    # have_known_vote = Vote.objects.filter(votetype=1)
    # not_understand_vote = Vote.objects.filter(votetype=2)
    #
    # context = {
    #     'understand_vote': understand_vote.len,
    #     'have_known_vote': have_known_vote.len,
    #     'not_understand_vote': not_understand_vote.len,
    # }

    # return render(request, template_name, context)
    return render(request, template_name)


def speaker_res(request):
    template_name = 'poll/speaker_res.html'

    return render(request, template_name)


def change_status(request):
    # TODO 任意のroom_idの取得
    room_info = RoomTable.objects.first()
    if request.POST['action'] == 'start-lec':
        VoteTable.objects.create(vote_type=0, vote_time=timezone.now(), slide_no=1, room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker'))
    elif request.POST['action'] == 'next-slide':
        current_slide = VoteTable.objects.order_by('slide_no').last()
        current_slide.slide_no += 1
        VoteTable.objects.create(vote_type=0, vote_time=timezone.now(), slide_no=current_slide.slide_no,
                                 room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker'))
    elif request.POST['action'] == 'fin-lec':
        VoteTable.objects.create(vote_type=-1, vote_time=timezone.now(), slide_no=1, room_id=room_info)
        return HttpResponseRedirect(reverse('poll:speaker_res'))


class VoteViewSet(viewsets.ModelViewSet):
    """
    現在の時間から過去30秒の票だけ表示する
    """
    late_limit_sec = 30
    # queryset = VoteTable.objects.filter(vote_time__gte=timezone.now() - timedelta(seconds=late_limit_sec))
    queryset = VoteTable.objects.all()
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
    コメントテーブルの内容をすべて返す
    （将来的に部屋やスライドの進行具合に合わせたコメント取得をしたい）
    """
    queryset = CommentTable.objects.all()
    serializer_class = CommentSerializer
