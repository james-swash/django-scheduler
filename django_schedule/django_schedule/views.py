from django.http import HttpResponse
from django.shortcuts import render

def about(request):
    # return HttpResponse("Hello world!")
    return render(request, 'about.html')

def home(request):
    #return HttpResponse("Home page!")
    return render(request, 'home.html')
