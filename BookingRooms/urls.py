"""BookingRooms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Conference.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", RoomsTodayListView.as_view(), name="all_rooms"),
    path("room/new/", TestView.as_view(), name="create_room"),
    path("room/modify/<int:id>/", TestView2.as_view(), name="modify_room"),
    path("room/delete/<int:id>/", TestView2.as_view(), name="delete_room"),
    path("room/<int:id>/", TestView2.as_view(), name="room_details"),

]
