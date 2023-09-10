from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.

def primero(request):
    return render(request,"home.html")

def secion(request):
    return render(request,"iniciar_secion.html")