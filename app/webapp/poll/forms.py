from django.forms import ModelForm
from .models import RoomTable


class RoomForm(ModelForm):
    """ルームのフォーム"""
    class Meta:
        model = RoomTable
        fields = ('room_name',)
