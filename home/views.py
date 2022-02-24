from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Room, Topic, Message
from .forms import RoomForm, UserRegistrationForm, UserForm
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

    topics = Topic.objects.all()[:3]

    room_count = rooms.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)) 



    return render(request, 'home/home.html', {
        'rooms':rooms,
        'topics':topics,
        'room_count': room_count,
        'room_messages': room_messages
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


def UserProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    return render(request, 'home/profile.html', {
        'user':user,
        'rooms': rooms,
        'topics':topics,
        'room_messages': room_messages
        })


@login_required(login_url='home:login')
def CreateRoom(request):
    template_name = 'home/room_form.html'
    form = RoomForm()
    topics = Topic.objects.all()


    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),

        )
        return redirect('home:home')
    
    
    return render(request, template_name, {
        'form':form,
        'topics':topics
        }
    )
        



@login_required(login_url='home:login')
def UpdateRoom(request, pk):
    template_name = 'home/room_form.html'
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    
    if request.user != room.host:
        return HttpResponse('Your not allowed here')
       
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home:home')
    return render(request, template_name, {
        'form':form,
        'topics':topics,
        'room':room
        })



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


@login_required(login_url='login')
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home:user-profile', pk=user.id)

    return render(request, 'home/update-user.html', {'form':form})



def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'home/topics.html', {'topics':topics})