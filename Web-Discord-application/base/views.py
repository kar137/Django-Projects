from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  #this helps to restrict the required views
from django.contrib.auth import authenticate, login, logout 
from .models import Room, Topic
from .form import RoomForm

# Create your views here.

def loginPage(Request):

    if Request.user.is_authenticated:
        return redirect('home')
    if Request.method == "POST":
        username = Request.POST.get('username')
        password = Request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(Request, 'User does not exist')
        
        user = authenticate(Request, username=username, password=password)
        if user is not None:
            login(Request, user)
            return redirect('home')
        else:
            messages.error(Request, 'Username or Password does not exist')
    
    return render(Request, 'base/login_register.html')

def logoutUser(Request):
    logout(Request)
    return redirect('home')

def home(Request):
    q = Request.GET.get('q') if Request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)

        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count}

    return render(Request, 'base/home.html', context)

def room(Request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(Request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(Request):
    form = RoomForm()

    if Request.method == 'POST':
        form = RoomForm(Request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(Request,'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(Request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)

    if Request.user != room.host:
            return HttpResponse('You are not allowed here!')

    if Request.method == "POST":
        form = RoomForm(Request.POST , instance= room)
        if form.is_valid():
            form.save()
            return redirect('home')
    

    context = {'form': form}
    return render(Request,'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(Request, pk):
    room = Room.objects.get(id = pk)

    if Request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(Request, 'base/delete.html', {'obj': room})