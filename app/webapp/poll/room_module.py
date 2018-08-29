from .models import RoomTable, SlideTable, ListenerTable


def make_room(name):
    room = RoomTable(room_name=name, password="default")
    room.save()


def join_room(name, ip):
    room = RoomTable.objects.get(room_name=name)
    room.num_listener += 1
    room.save()
    listener = ListenerTable(listener_ip=ip, room_id=room)
    listener.save()
