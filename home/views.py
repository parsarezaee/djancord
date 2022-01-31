from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
from django.views import View



def home(request):
    rooms = Room.objects.all()
    return render(request, 'home/home.html', {'rooms':rooms})


def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'home/room.html', {'room':room})



class CreatRoom(View):
    template_name = 'home/room_form.html'
    
    def get(self, request):
        form = RoomForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        if request.method == 'POST':
            form = RoomForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home:home')


class UpdateRoom(View):
    template_name = 'home/room_form.html'

    def get(self, request, pk):
        room = Room.objects.get(id=pk)
        form = RoomForm(instance=room)
        return render(request, self.template_name, {'form':form})

    def post(self, request, pk):
        room = Room.objects.get(id=pk)
        if request.method == 'POST':
             form = RoomForm(request.POST, instance=room)
             if form.is_valid():
                 form.save()
                 return redirect('home:home')

