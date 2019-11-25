from _operator import itemgetter
from datetime import datetime

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.views import View
from psycopg2._psycopg import IntegrityError

from Conference.models import *

# Create your tests here.
from Conference.utils import validate_positive_int, messages, booked_rooms_ids, create_redirect_param


class TestView(View):
    def get(self, request):
        return render(request, "BookingRooms/test1.html")


class TestView2(View):
    def get(self, request, id, day):
        return render(request, "BookingRooms/test1.html")


class RoomsTodayListView(View):
    def get(self, request):
        day = datetime.today().strftime("%Y-%m-%d")
        rooms = Room.objects.all().order_by('name')
        bookings = Booking.objects.filter(date=day)
        booked_ids = []
        for booking in bookings:
            booked_ids.append(booking.room_id)
        paginator = Paginator(rooms, 20)  # Show 10 recipes per page
        page = request.GET.get('page')
        rooms = paginator.get_page(page)
        return render(request, 'BookingRooms/app-rooms.html',
                      {"day": day, "object_list": rooms, "booked_ids": booked_ids})

    def post(self, request):
        day = datetime.today().strftime("%Y-%m-%d")
        booked_ids = []
        object_list = Room.objects.all()
        if "search_by_day" in request.POST and request.POST.get("searched_day") is "":
            return render(request, 'BookingRooms/app-rooms.html',
                          {"object_list": object_list})
        if "search_by_day" in request.POST and request.POST.get("searched_day") is not "":
            day = request.POST.get("searched_day")
            booked_ids = booked_rooms_ids(day)
            object_list = Room.objects.all().order_by('name')
            paginator = Paginator(object_list, 20)  # Show 10 recipes per page
            page = request.GET.get('page')
            object_list = paginator.get_page(page)
            return render(request, 'BookingRooms/app-rooms.html',
                          {"day": day, "object_list": object_list, "booked_ids": booked_ids})



        else:
            side_day = request.POST.get("side_day")
            searched_name = request.POST.get("searched_name")
            searched_size = request.POST.get("searched_size")
            if side_day:
                booked_ids = booked_rooms_ids(side_day)
                object_list = object_list.all().exclude(id__in=booked_ids)
            if searched_name:
                object_list = object_list.filter(name__icontains=searched_name)
            if searched_size:
                object_list = object_list.filter(size__gte=searched_size)
            if "searched_projector" in request.POST:
                searched_projector = "With"
                object_list = object_list.filter(projector=True)
            else:
                searched_projector = "Without"
                object_list = object_list.filter(projector=False)
            paginator = Paginator(object_list, 20)  # Show 10 recipes per page
            page = request.GET.get('page')
            object_list = paginator.get_page(page)
            return render(request, 'BookingRooms/app-rooms.html',
                          {"object_list": object_list, "booked_ids": booked_ids, "side_day": side_day,
                           "searched_size": searched_size, "searched_name": searched_name,
                           "searched_projector": searched_projector})


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


class RoomModifyView(View):

    def get(self, request, id):
        room = Room.objects.get(id=id)
        return render(request, "BookingRooms/app-modify-room.html", {'room_name': room.name,
                                                                     'room_projector': room.projector,
                                                                     'room_size': room.size})

    def post(self, request, id):
        room_name = request.POST.get('room_name')
        room_projector = request.POST.get('room_projector')
        if room_projector == 'True':
            room_projector = True
        else:
            room_projector = False
        room_size = request.POST.get('room_size')
        room_size = validate_positive_int(room_size)
        if not room_size or "" in (room_name, room_projector):
            return render(request, 'BookingRooms/app-modify-room.html', {'room_name': room_name,
                                                                         'room_projector': room_projector,
                                                                         'room_size': room_size,
                                                                         'message': messages['wrong_data']})
        room = Room.objects.get(id=id)
        room.name = room_name
        room.size = room_size
        room.projector = room_projector
        room.save()
        return redirect('all_rooms')


class RoomBookView(View):
    default_day=datetime.today()
    def get(self, request, id, day=default_day):
        today = datetime.today()
        room = Room.objects.get(id=id)
        bookings = Booking.objects.filter(room=id, date__gte=today)
        return render(request, "BookingRooms/app-room-book.html", {'room_name': room.name, "room_id": room.id,
                                                                   "day": day, "bookings": bookings, "today": today})

    def post(self, request, id, day=default_day):
        today = datetime.today()
        booking_date = request.POST.get('date')
        comment = request.POST.get('comment')
        bookings_of_current_room = []
        room = Room.objects.get(id=id)
        bookings = Booking.objects.filter(room=id)
        for booking in bookings:
            bookings_of_current_room.append(booking.date.strftime("%Y-%m-%d"))
        if booking_date in bookings_of_current_room:
            return render(request, "BookingRooms/app-room-book.html",
                          {"room_name": room.name, "day": booking_date, "bookings": bookings, "today": today,
                           "message": messages['taken_date']})
        if booking_date < today.strftime("%Y-%m-%d") or not booking_date:
            return render(request, "BookingRooms/app-room-book.html",
                          {"room_name": room.name, "day": booking_date, "bookings": bookings, "today": today,
                           "message": messages['wrong_data']})
        Booking.objects.create(room_id=id, date=booking_date, comment=comment)
        bookings = Booking.objects.filter(room=id)
        for booking in bookings:
            bookings_of_current_room.append(booking.date.strftime("%Y-%m-%d"))
        message = f"Salkę {room.name} zarezerwowano na dzień {booking_date}"
        return render(request, "BookingRooms/app-room-book.html",
                      {"room_name": room.name, "day": booking_date, "bookings": bookings, "today": today,
                       "message": message})