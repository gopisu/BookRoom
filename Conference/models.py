from django.db import models


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=64)
    size = models.PositiveIntegerField(null=True)
    projector = models.BooleanField(null=True)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        unique_together = (
            "date",
            "room",
        )
