from django.contrib import admin
from .models import RoomTable, VoteTable, CommentTable

# RoomTable, VoteTable, CommentTableをadminサイトから触れられるように登録
admin.site.register(RoomTable)
admin.site.register(VoteTable)
admin.site.register(CommentTable)
