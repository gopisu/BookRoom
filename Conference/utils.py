# Universal functions
from django.urls import reverse
from urllib.parse import urlencode

from Conference.models import *

messages = {
    'already_logged_in': "Użytkownik jest już zalogowany!",
    'wrong_user_data': "Zła nazwa użytkownika lub hasło, spróbuj ponownie!",
    'wrong_data': "Proszę wypełnij poprawnie wszystkie pola.",
    'user_exists': "Użytkownik już istnieje, wybierz inny login/email",
}


def count(model):
    return model.objects.all().count()


def validate_int(variable):
    try:
        var2 = int(variable)
    except ValueError:
        return False
    return var2


def validate_positive_int(number):
    number = validate_int(number)
    if number < 0 and number:
        return False
    return number


def create_redirect_param(view_name, param):
    base_url = reverse(view_name)
    message_text = param
    message = urlencode({'message': message_text})
    return f'{base_url}?{message}'


def booked_rooms_ids(day):
    bookings = Booking.objects.filter(date=day)
    booked_ids = []
    for booking in bookings:
        booked_ids.append(booking.room_id)
    return booked_ids
