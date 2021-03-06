from django.contrib import admin
from .models import RoomTable, SlideTable, VoteTable, CommentTable


class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_name', 'password', 'num_listener',)  # 一覧に出したい項目
    list_display_links = ('room_name',)  # 修正リンクでクリックできる項目


class SlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'slide_no', 'start_time', 'end_time', 'room_id',)  # 一覧に出したい項目
    list_display_links = ('slide_no', 'start_time', 'end_time',)  # 修正リンクでクリックできる項目


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'vote_type', 'vote_time', 'slide_id',)  # 一覧に出したい項目
    list_display_links = ('vote_type', 'vote_time')  # 修正リンクでクリックできる項目


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment_text', 'comment_time', 'slide_id',)  # 一覧に出したい項目
    list_display_links = ('comment_text', 'comment_time')  # 修正リンクでクリックできる項目


# RoomTable, VoteTable, CommentTableをadminサイトから触れられるように登録
admin.site.register(RoomTable, RoomAdmin)
admin.site.register(SlideTable, SlideAdmin)
admin.site.register(VoteTable, VoteAdmin)
admin.site.register(CommentTable, CommentAdmin)
