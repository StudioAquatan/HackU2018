from .models import RoomTable, VoteTable, CommentTable

from django.utils import timezone

def set_vote():
    room = RoomTable.objects.get(id=1)
    vote = VoteTable(vote_time=timezone.now(), slide_no=0)
    vote.room_id = room
    # save the object into the database.
    return vote


def button1():
    vote = set_vote()
    vote.vote_type = 1;
    vote.save()
    return


def button2():
    vote = set_vote()
    vote.vote_type = 2;
    vote.save()
    return


def button3():
    vote = set_vote()
    vote.vote_type = 3;
    vote.save()
    return
