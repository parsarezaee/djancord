from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login




def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.error(request, 'Username or password does not exist')


    return render(request, 'home/login_register.html')



def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()

    room_count = rooms.count()

    return render(request, 'home/home.html', {
        'rooms':rooms,
        'topics':topics,
        'room_count': room_count
        })


def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'home/room.html', {'room':room})



class CreateRoom(View):
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




class DeleteRoom(View):
    template_name = 'home/delete.html'
    
    def get(self, request, pk):
        room = Room.objects.get(id=pk) 

        return render(request, self.template_name, {'obj':room})
    

    def post(self, request, pk):
        room = Room.objects.get(id=pk) 

        if request.method == 'POST':
            room.delete()
            return redirect('home:home')


