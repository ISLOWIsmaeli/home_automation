from django.shortcuts import render
from django.http import HttpResponse
from mqtt import listener
# Create your views here.
# def index(request):
#     return HttpResponse("I am working")
def home(response):
    return render(response, "monitor/home.html",{})