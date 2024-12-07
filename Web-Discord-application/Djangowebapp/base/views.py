from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

rooms = [
    {'id':1, 'name': 'Lets learn python!'},
    {'id':2, 'name': 'Design with me!'},
    {'id':3, 'name': 'Frontend Developers'},
]

def home(Request):
    context = {'rooms':rooms}
    return render(Request, 'base/home.html', context)
def room(Request):
    return render(Request, 'room.html')