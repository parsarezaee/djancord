from django.contrib import admin
from .models import Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_filter = ('updated',)
    prepopulated_fields = {'slug':('name',)}