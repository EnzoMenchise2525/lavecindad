from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

def primero(request):
    return render(request,"iniciar_secion.html")

def bienvenida(request):
    return render(request,"bienvenida.html")

