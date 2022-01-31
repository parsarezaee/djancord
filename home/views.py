from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home/home.html', {'rooms':rooms})


def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'home/room.html', {'room':room})



def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')
            
    return render(request, 'home/room_form.html', {'form':form})


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home:home')
    return render(request, 'home/room_form.html', {'form':form})