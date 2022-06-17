from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def indexview(request):
    return render(request, 'register/index.html')


def detailsview(request):
    return render(request, 'register/details.html')


def addview(request):
    return render(request, 'register/add.html')


def editview(request):
    return render(request, 'register/edit.html')
