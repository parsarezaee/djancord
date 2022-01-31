from django.shortcuts import render
from .models import Room


rooms = [
    {'id': 1, 'name':'python challenge'},
    {'id': 2, 'name':'cpp challenge in 100 days'},
    {'id': 3, 'name':'golang challenge in 50 days'}
]

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home/home.html', {'rooms':rooms})


def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    return render(request, 'home/room.html', {'room':room})