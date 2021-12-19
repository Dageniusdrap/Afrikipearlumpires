from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.db.models import Q
from django.http import HttpResponse

from .forms import RoomForm, UserForm, MyUserCreationForm
from .models import Rooms, Topic, Message, User

# Create your views here.

# rooms = [
#     {'id':1, 'name':"Welcome at Wakanda Land!!"},
#     {'id':2, 'name':"Lets do Wakanda Things!!"},
#     {'id':3, 'name':"In Wakanda Kiafrika way!!"},
# ]


def loginPage(request):
    page = 'Login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user =User.objects.get(email=email)
        except:
            messages.error(request, 'User does not Exist.')
        user = authenticate(request, password=password, email=email)
        

        if user is not None:
            login(request,user)
            return redirect("home")

        else:
            messages.error(request, 'Username OR PassWord does not Exist.')

    context = {'page':page}
    return render(request, 'wakanda/Login_register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def RegisterPage(request):
   
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something Went Wrong During Registration!!')



    return render(request, 'wakanda/Login_register.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    rooms = Rooms.objects.filter(
        Q(topic__name__icontains =q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
        )

    topics = Topic.objects.all()[0:3]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count, 'room_messages':room_messages}
    return render(request, 'wakanda/home.html', context)

def room(request, pk):
    room = Rooms.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body = request.POST.get('body')
        )

        room.participants.add(request.user)

        return redirect('room', pk=room.id)


    context = {'room':room, 'room_messages':room_messages, 'participants':participants}

    return render(request, 'wakanda/room.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.rooms_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'wakanda/profile.html', context)

@login_required(login_url='Login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        
        Rooms.objects.create(
            host=request.user,
            topic= topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()

        return redirect('home')
    context = {'form': form, 'topics':topics}

    return render(request, 'wakanda/room_form.html', context)

@login_required(login_url='Login')
def updateRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Sorry, you cant make Updates!!')

    if request.method=='POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        return redirect('home')
            
    context = {'form': form, 'topics':topics, 'room':room }
    return render(request, 'wakanda/room_form.html', context)

@login_required(login_url='Login')
def deleteROOM(request, pk):
    room = Rooms.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("Sorry, You cant delete this content.")
    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'wakanda/delete.html', {'obj':room})


@login_required(login_url='Login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("Sorry, You cant delete this content.")
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'wakanda/delete.html', {'obj':message})


@login_required(login_url='Login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'wakanda/update-user.html', {'form':form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'wakanda/topics.html', {'topics':topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'wakanda/activity.html', {'room_messages':room_messages})