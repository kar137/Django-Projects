from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(Request):
    return render(Request, 'home.html')
def room(Request):
    return render(Request, 'room.html')