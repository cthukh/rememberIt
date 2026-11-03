from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CrearFuncionarioForm, CrearResidenteForm
from funcionarios.models import Funcionario

@login_required
def inicio_admin(request):
    user = request.user
    if user.is_superuser == True and user.is_active == True:
        funcionarios = Funcionario.objects.all()
        return render(request,  'inicio_admin.html', {'funcionarios':funcionarios})

    elif user.is_superuser == False or user.is_active == False:
        return redirect("home")


# ----------------------------------- funcionarios ----------------------------------- 
@login_required
def crear_funcionario(request):
    user = request.user
    if user.is_superuser == True and user.is_active == True:
        if request.method == 'POST':
            form = CrearFuncionarioForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Cuenta creada con exito.")
                return redirect("funcionarios:funcionario")
            else:
                messages.error(request, "¡Ocurrio un error al crear la cuenta!")
        else:
            form = CrearFuncionarioForm()
        return render(request,"crear_funcionario.html", {"form":form})

    elif user.is_superuser == False or user.is_active == False:
        return redirect("home")


# ----------------------------------- residentes -----------------------------------
@login_required
def crear_residente(request):
    user = request.user
    if user.is_superuser == True and user.is_active == True:
        if request.method == 'POST':
            form = CrearResidenteForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Cuenta creada con exito.")
                return redirect('residentes:inicio_residentes')
            else:
                messages.error(request, "¡Ocurrio un error al crear la cuenta!")
        else:
            form = CrearResidenteForm()
        return render(request, 'crear_residente.html', {'form': form})

    elif user.is_superuser == False or user.is_active == False:
        return redirect("home")

















@login_required
def modificar_funcionario(request):
    if request.method != "POST":
        return redirect("funcionarios:funcionario")

    form = ActuaFuncionarioForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Tus datos de perfil se actualizaron correctamente.")
        return redirect("funcionarios:funcionario")

    return render(request, "perfil_funcionario.html", {"datUsu": request.user, "form": form})