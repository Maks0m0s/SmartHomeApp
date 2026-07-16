from django.contrib.auth.models import User
from main.models import Category, Floor, Room, Device


def get_categories():
    categories = Category.objects.all()
    return {"categories": categories}


def get_category_objects(name):
    category = Category.objects.filter(name=name).first()
    if not category:
        return []
    return list(category.objs.all())


def get_floors():
    return Floor.objects.all().order_by("order")


def get_users():
    return User.objects.all()


def get_rooms_for_floor(floor_id):
    floor = Floor.objects.get(id=floor_id)
    return floor.rooms.all()


def get_devices_for_room(room_id):
    room = Room.objects.get(id=room_id)
    return room.devices.all()


def get_devices_for_user(user_id):
    return Device.objects.filter(creator_id=user_id)


def get_devices_by_active_state():
    return Device.objects.filter(is_active=True)


def get_devices_by_inactive_state():
    return Device.objects.filter(is_active=False)
