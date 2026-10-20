from django.shortcuts import render
from .forms import ResidenteForm
# Create your views here.

from django.shortcuts import render, redirect
from .models import ResidenteForm

def registrar_residente(request):
    if request.method == 'POST':
        form = ResidenteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_residentes')
    else:
        form = ResidenteForm()
    return render(request, 'funcionarios/templates/registro.html', {'form': form})