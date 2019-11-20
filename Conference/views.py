from django.http import HttpResponse
from django.shortcuts import render
from django.test import TestCase
from django.views import View

# Create your tests here.

class TestView(View):
    def get(self, request):
        return render(request, "BookingRooms/test1.html")
