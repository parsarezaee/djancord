from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, UserRegistrationForm
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required





def loginPage(request):


    if request.user.is_authenticated:
        return redirect('home:home')


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




def logoutUser(request):
    logout(request)
    return redirect('home:home')




def SignupView(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user but avoid saving yet
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            return render(request, 'registration/signup_done.html', {
                'new_user': new_user
            })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/signup.html', 
        {'user_form': user_form})





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
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('home:room', pk=room.id)

    return render(request, 'home/room.html', {
        'room':room,
        'room_messages':room_messages,
        'participants': participants
    }
    )





@login_required(login_url='home:login')
def CreateRoom(request):
    template_name = 'home/room_form.html'
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:home')
    return render(request, template_name, {'form':form})
        



@login_required(login_url='home:login')
def UpdateRoom(request, pk):
    template_name = 'home/room_form.html'
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    
    if request.user != room.host:
        return HttpResponse('Your not allowed here')
       
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home:home')
    return render(request, template_name, {'form':form})



@login_required(login_url='home:login')
def DeleteRoom(request, pk):
    template_name = 'home/delete.html'
    room = Room.objects.get(id=pk) 
    if request.user != room.host:
        return HttpResponse("You are not allowed here!")

    if request.method == 'POST':
        room.delete()
        return redirect('home:home')
    return render(request, template_name, {'obj':room})




@login_required(login_url='home:login')
def DeleteMessage(request, pk):
    template_name = 'home/delete.html'
    message = Message.objects.get(id=pk) 


    if request.user != message.user:
        return HttpResponse("You are not allowed here!")


    if request.method == 'POST':
        message.delete()
        return redirect('home:home')
    return render(request, template_name, {'obj':message})

