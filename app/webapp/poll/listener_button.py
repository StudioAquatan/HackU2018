from .models import RoomTable, VoteTable, CommentTable, SlideTable

from django.utils import timezone
from django.db import models


def set_vote():
    room = RoomTable.objects.get(id=1)
    # room情報からslide情報を取得
    slide = SlideTable.objects.filter(room_id=room).latest('start_time')
    # slide情報からvoteを作成
    vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
    return vote


def button1():
    vote = set_vote()
    vote.vote_type = 1
    vote.save()


def button2():
    vote = set_vote()
    vote.vote_type = 2
    vote.save()


def button3():
    vote = set_vote()
    vote.vote_type = 3
    vote.save()


def comment_submit(input_comment):
    room = RoomTable.objects.get(id=1)
    # room情報からslide情報を取得
    slide = SlideTable.objects.filter(room_id=room).latest('start_time')
    # slide情報からcommentを作成
    comment = CommentTable(comment_text=input_comment, comment_time=timezone.now(), slide_id=slide)
    comment.save()