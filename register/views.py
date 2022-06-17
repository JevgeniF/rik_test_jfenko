from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def indexview(request):
    return HttpResponse("Avaleht")


def detailsview(request):
    return HttpResponse("Osaühingu andmete vaade")


def addview(request):
    return HttpResponse("Osaühingu asutamise vorm")


def editview(request):
    return HttpResponse("Osaühingu osakapitali suurendamise vorm")