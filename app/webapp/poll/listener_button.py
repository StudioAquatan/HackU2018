from .models import RoomTable, SlideTable, VoteTable, CommentTable, ListenerTable

from django.utils import timezone


def set_vote(ip):
    # ipアドレスからlistener情報を取得
    listener = ListenerTable.objects.get(listener_ip=ip)
    # listener情報からroom情報を取得
    room = RoomTable.objects.get(id=listener.room_id)
    # room情報からslide情報を取得
    slide = SlideTable.objects.filter(room_id=room).latest(SlideTable.start_time)
    # slide情報からvoteを作成
    vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
    # save the object into the database.
    return vote


# それぞれのボタンに応じてvote_typeを代入
def button1(ip):
    vote = set_vote(ip)
    vote.vote_type = 1
    vote.save()
    return


def button2(ip):
    vote = set_vote(ip)
    vote.vote_type = 2
    vote.save()
    return


def button3(ip):
    vote = set_vote(ip)
    vote.vote_type = 3
    vote.save()
    return
