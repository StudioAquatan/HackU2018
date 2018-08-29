from rest_framework import serializers

from .models import VoteTable, RoomTable, CommentTable, SlideTable


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTable
        fields = ('room_name', 'password', 'num_listener')


class SlideSerializer(serializers.ModelSerializer):
    room_id = RoomSerializer()

    class Meta:
        model = SlideTable
        fields = ('slide_no', 'start_time', 'end_time', 'room_id')


class VoteSerializer(serializers.ModelSerializer):
    slide_id = SlideSerializer()

    class Meta:
        model = VoteTable
        fields = ('vote_type', 'vote_time', 'slide_id')


class CommentSerializer(serializers.ModelSerializer):
    slide_id = SlideSerializer()

    class Meta:
        model = CommentTable
        fields = ('comment_text', 'comment_time', 'slide_id')
