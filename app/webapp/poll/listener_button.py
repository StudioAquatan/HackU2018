from .models import RoomTable, VoteTable, CommentTable, SlideTable

from django.utils import timezone


def get_slide(get_id):
    # room_idからroomレコードを取得
    room = RoomTable.objects.get(id=get_id)
    # room情報からslideレコードを取得
    if SlideTable.objects.filter(room_id=room).exists():
        slide = SlideTable.objects.filter(room_id=room).latest('start_time')
        return slide
    else:
        # slideがなければFalseを返す
        return False


def button1(room_id):
    slide = get_slide(room_id)
    # slideがFalseでなければ
    if slide:
        # slide情報からvoteを作成
        vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
        vote.vote_type = 1
        vote.save()
        return True
    else:
        return False


def button2(room_id):
    slide = get_slide(room_id)
    # slideがFalseでなければ
    if slide:
        # slide情報からvoteを作成
        vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
        vote.vote_type = 2
        vote.save()
        return True
    else:
        return False


def button3(room_id):
    slide = get_slide(room_id)
    # slideがFalseでなければ
    if slide:
        # slide情報からvoteを作成
        vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
        vote.vote_type = 3
        vote.save()
        return True
    else:
        return False


def comment_submit(input_comment, room_id):
    slide = get_slide(room_id)
    # slideがFalseでなければ
    if slide:
        # slide情報からcommentを作成
        comment = CommentTable(comment_text=input_comment, comment_time=timezone.now(), slide_id=slide)
        comment.save()
        return True
    else:
        return False
