from _operator import itemgetter
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from Conference.models import *

# Create your tests here.
from Conference.utils import validate_positive_int, messages


class TestView(View):
    def get(self, request):
        return render(request, "BookingRooms/test1.html")


class TestView2(View):
    def get(self, request, id):
        return render(request, "BookingRooms/test1.html")


class RoomsTodayListView(View):
    def get(self, request):
        rooms = Room.objects.all().order_by('name')
        date = datetime.today()
        all_rooms_today = []
        for room in rooms:
            status_today = Booking.objects.filter(room=room.id, date=date)
            all_rooms_today.append((room, status_today))
        paginator = Paginator(all_rooms_today, 10)  # Show 10 recipes per page
        page = request.GET.get('page')
        all_rooms_today = paginator.get_page(page)
        return render(request, 'BookingRooms/app-rooms.html', {"object_list": all_rooms_today})


class RoomDetailsView(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)
        date = datetime.today()
        bookings = Booking.objects.filter(room=id, date__gte=date)
        return render(request, 'BookingRooms/app-room-details.html', {"room": room, "bookings": bookings})


class RoomAddView(View):

    def get(self, request):
        return render(request, "BookingRooms/app-add-room.html")

    def post(self, request):
        room_name = request.POST.get('room_name')
        room_projector = request.POST.get('room_projector')
        if room_projector == 'True':
            room_projector = True
        else:
            room_projector = False
        room_size = request.POST.get('room_size')
        room_size = validate_positive_int(room_size)
        if not room_size or "" in (room_name, room_projector):
            return render(request, 'BookingRooms/app-add-room.html', {'room_name': room_name,
                                                                      'room_projector': room_projector,
                                                                      'room_size': room_size,
                                                                      'message': messages['wrong_data']})
        Room.objects.create(name=room_name, size=room_size, projector=room_projector)
        return redirect('all_rooms')
