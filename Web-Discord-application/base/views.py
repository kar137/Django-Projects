from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required  # Ensures only logged-in users can access certain views
from django.contrib.auth import authenticate, login, logout  # Handles user authentication
from django.contrib.auth.forms import UserCreationForm  #Handles the user creation form for register
from .models import Room, Topic  # Imports models for database interaction
from .form import RoomForm  # Imports custom form for Room creation and updates

#create your views here

# Function to handle user login
def loginPage(Request):
    page = 'login'

    # Redirect authenticated users directly to the homepage
    if Request.user.is_authenticated:
        return redirect('home')

    # Handle login form submission
    if Request.method == "POST":
        username = Request.POST.get('username').lower()  # Get username from the form
        password = Request.POST.get('password')  # Get password from the form

        try:
            user = User.objects.get(username=username)  # Check if user exists
        except:
            messages.error(Request, 'User does not exist')  # Show error if user not found
        
        # Authenticate the user
        user = authenticate(Request, username=username, password=password)
        if user is not None:  # If authentication is successful
            login(Request, user)  # Log in the user
            return redirect('home')  # Redirect to homepage
        else:
            messages.error(Request, 'Username or Password does not exist')  # Show error if login fails
    
    context = {'page': page}

    # Render the login/register page
    return render(Request, 'base/login_register.html', context)

# Function to handle user logout
def logoutUser(Request):
    logout(Request)  # Log out the user
    return redirect('home')  # Redirect to homepage

# Function to render the registration page (currently only renders the form)
def registerPage(Request):
    form = UserCreationForm()

    if Request.method == "POST":
        form = UserCreationForm(Request.POST)
        if form.is_valid():
            user = form.save(commit=False)  #create an instance of the form but doesnot save to the database
            user.username = user.username.lower()  #converts to lower case
            user.save()  #finally saves the form
            login(Request, user)  # log in the user
            return redirect('home')  #returns to home page
        else:
            messages.error(Request, "An error occurred during registration! ")

    

    return render(Request, 'base/login_register.html', {'form': form})

# Function to render the homepage
def home(Request):
    # Search functionality using query parameters
    q = Request.GET.get('q') if Request.GET.get('q') != None else ''

    # Filter rooms based on topic, name, or description
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()  # Get all topics
    room_count = rooms.count()  # Count filtered rooms

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}

    # Render the homepage with the rooms and topics
    return render(Request, 'base/home.html', context)

# Function to render a specific room's details
def room(Request, pk):
    room = Room.objects.get(id=pk)  # Get the room by primary key (id)
    context = {'room': room}
    return render(Request, 'base/room.html', context)

# Function to create a new room (restricted to logged-in users)
@login_required(login_url='login')
def createRoom(Request):
    form = RoomForm()  # Instantiate an empty RoomForm

    if Request.method == 'POST':  # Handle form submission
        form = RoomForm(Request.POST)  # Populate form with POST data
        if form.is_valid():  # Validate form
            form.save()  # Save the new room to the database
            return redirect('home')  # Redirect to homepage

    context = {'form': form}
    return render(Request, 'base/room_form.html', context)

# Function to update an existing room (restricted to the room's host)
@login_required(login_url='login')
def updateRoom(Request, pk):
    room = Room.objects.get(id=pk)  # Get the room by primary key (id)
    form = RoomForm(instance=room)  # Pre-fill form with room's data

    if Request.user != room.host:  # Restrict access to the room's host
        return HttpResponse('You are not allowed here!')

    if Request.method == "POST":  # Handle form submission
        form = RoomForm(Request.POST, instance=room)  # Update the room instance
        if form.is_valid():  # Validate form
            form.save()  # Save changes to the database
            return redirect('home')  # Redirect to homepage

    context = {'form': form}
    return render(Request, 'base/room_form.html', context)

# Function to delete a room (restricted to the room's host)
@login_required(login_url='login')
def deleteRoom(Request, pk):
    room = Room.objects.get(id=pk)  # Get the room by primary key (id)

    if Request.method == 'POST':  # Handle delete confirmation
        room.delete()  # Delete the room from the database
        return redirect('home')  # Redirect to homepage

    # Render the delete confirmation page
    return render(Request, 'base/delete.html', {'obj': room})