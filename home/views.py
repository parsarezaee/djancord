from django.shortcuts import render
from .models import Room


def home(request):
    rooms = Room.objects.all()
    return render(request, 'home/home.html', {'rooms':rooms})


def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'home/room.html', {'room':room})



def createRoom(request):

    return render(request, 'home/room_form.html')