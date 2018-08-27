from rest_framework import serializers

from .models import VoteTable, RoomTable, CommentTable


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteTable
        fields = ('vote_type', 'vote_time', 'slide_no', 'room_id')


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTable
        fields = ('room_name', 'password', 'num_listener')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentTable
        fields = ('comment_text', 'comment_time', 'slide_no', 'room_id')
