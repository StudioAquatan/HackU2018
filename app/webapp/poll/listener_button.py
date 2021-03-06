from .models import RoomTable, VoteTable, CommentTable, SlideTable

from django.utils import timezone


def get_slide(get_id):
    # room_idからroomレコードを取得
    room = RoomTable.objects.get(id=get_id)
    # room情報からslideレコードを取得
    if SlideTable.objects.filter(room_id=room).exists():
        slide = SlideTable.objects.filter(room_id=room).latest('start_time')
        if slide.end_time is None:
            return slide
        else:
            # 最新のスライドが終了していれば講義が終了していると判断して-2を返す
            return -2
    else:
        # slideがなければ-1を返す
        return -1


def button1(room_id):
    slide = get_slide(room_id)
    if slide != -1 and slide != -2:
        # slideが-1または-2でなければ
        # slide情報からvoteを作成
        vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
        vote.vote_type = 1
        vote.save()
        return 1
    else:
        return slide


def button2(room_id):
    slide = get_slide(room_id)
    if slide != -1 and slide != -2:
        # slideが-1または-2でなければ
        # slide情報からvoteを作成
        vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
        vote.vote_type = 2
        vote.save()
        return 1
    else:
        return slide


def button3(room_id):
    slide = get_slide(room_id)
    if slide != -1 and slide != -2:
        # slideが-1または-2でなければ
        # slide情報からvoteを作成
        vote = VoteTable(vote_time=timezone.now(), slide_id=slide)
        vote.vote_type = 3
        vote.save()
        return 1
    else:
        return slide


def comment_submit(input_comment, room_id):
    slide = get_slide(room_id)
    if slide != -1 and slide != -2:
        # slideが-1または-2でなければ
        # slide情報からcommentを作成
        comment = CommentTable(comment_text=input_comment, comment_time=timezone.now(), slide_id=slide)
        comment.save()
        return 2
    else:
        return slide
