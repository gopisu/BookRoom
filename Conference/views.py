from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from Conference.models import *


# Create your tests here.

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
            status_today = Booking.objects.filter(room = room.id, date=date)
            all_rooms_today.append((room, status_today))
        paginator = Paginator(all_rooms_today, 10)  # Show 10 recipes per page
        page = request.GET.get('page')
        all_rooms_today = paginator.get_page(page)
        return render(request, 'BookingRooms/app-rooms.html', {"object_list": all_rooms_today})
