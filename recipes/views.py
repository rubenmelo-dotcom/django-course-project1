from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse('Minha HOME do APP')

def sobre(request):
    return HttpResponse('Minha página SOBRE do APP')

def contato(request):
    return HttpResponse('Minha página CONTATO do APP')