from django.db import models


class RoomTable(models.Model):
    """
    ルームのモデル
    """
    # ルーム名
    room_name = models.CharField(max_length=32)
    # パスワード
    password = models.CharField(max_length=32)
    # リスナーの人数
    num_listener = models.IntegerField(default=0)

    def __str__(self):
        return self.room_name


class SlideTable(models.Model):
    """
    スライドのモデル
    """
    # スライド番号
    slide_no = models.IntegerField(default=0)
    # スライドの開始時間
    start_time = models.DateTimeField('slide start time')
    # スライドの終了時間
    end_time = models.DateTimeField('slide end time')
    # ルームID
    room_id = models.ForeignKey(RoomTable, on_delete=models.CASCADE)


class VoteTable(models.Model):
    """
    票のモデル
    """
    # 票の種類
    vote_type = models.IntegerField()
    # 票の送信時刻
    vote_time = models.DateTimeField('date published')
    # 投票時のスライドID
    slide_id = models.ForeignKey(SlideTable, on_delete=models.CASCADE)
    # ルームID
    room_id = models.ForeignKey(RoomTable, on_delete=models.CASCADE)


class CommentTable(models.Model):
    """
    コメントのモデル
    """
    # コメントの内容
    comment_text = models.CharField(max_length=256)
    # コメントの送信時刻
    comment_time = models.DateTimeField('date published')
    # コメント送信時のスライドID
    slide_id = models.ForeignKey(SlideTable, on_delete=models.CASCADE)
    # ルームID
    room_id = models.ForeignKey(RoomTable, on_delete=models.CASCADE)
