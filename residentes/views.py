from django.shortcuts import render


def inicio_residentes(request):
    return render(request, 'inicio_residentes.html')


def crear_residente():
    return

def update_residente(request):
    return render(request, 'updateresidente.html')