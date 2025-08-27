from django.contrib import admin
from .models import Room, Client, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'type', 'capacity', 'price_per_night', 'is_active')
    list_filter = ('type', 'is_active')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'room', 'check_in', 'check_out', 'status', 'created_at')
    list_filter = ('status', 'room')
