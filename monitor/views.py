from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# from mqtt import listener
# Create your views here.
# def index(request):
#     return HttpResponse("I am working")
def home(request: HttpRequest, *args, **kwargs):
    if request.method == "POST":
        print(request.POST)
    return render(request, "monitor/home.html",{})