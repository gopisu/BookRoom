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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from Conference.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RoomsTodayListView.as_view(), name="all_rooms"),
    path("index/", RoomsTodayListView.as_view(), name="all_rooms"),
    path("room/new/", RoomAddView.as_view(), name="create_room"),
    path("room/modify/<int:id>/", RoomModifyView.as_view(), name="modify_room"),
    path("room/delete/<int:id>/", RoomDeleteView.as_view(), name="delete_room"),
    url(
        r"^room/book/(?P<id>[0-9]+)/(?P<day>[0-9]{4}-?[0-9]{2}-?[0-9]{2})/$",
        RoomBookView.as_view(),
        name="room_book",
    ),
    url(r"^room/book/(?P<id>[0-9]+)/$", RoomBookView.as_view(), name="room_book"),
    url(r"^room/book/", RoomBookView.as_view(), name="room_book"),
    path("room/<int:id>/", RoomDetailsView.as_view(), name="room_details"),
]
