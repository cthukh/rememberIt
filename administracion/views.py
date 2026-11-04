from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CrearFuncionarioForm, CrearResidenteForm, ActualizarFuncionarioForm
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
                return redirect("administracion:inicio_admin")
            else:
                messages.error(request, "¡Ocurrio un error al crear la cuenta!")
                return redirect("administracion:inicio_admin")
        else:
            form = CrearFuncionarioForm()
        return render(request,"crear_funcionario.html", {"form":form})

    elif user.is_superuser == False or user.is_active == False:
        return redirect("home")


@login_required
def modificar_funcionario(request, uuid):
    if user.is_superuser == True and user.is_active == True:
        user = get_object_or_404(Funcionario, uuid=uuid)
        form = ActualizarFuncionarioForm(request.POST, instance=user)

        if request.method != "POST":
            return redirect("funcionarios:perfil", uuid=uuid)

                
        if form.is_valid():
            form.save()
            messages.success(request, "Los datos de perfil se actualizaron correctamente.")
            return redirect("funcionarios:perfil", uuid=uuid )

        return render(request, "perfil_funcionario.html", {"datUsu": user, "form": form})

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
                return redirect('residentes:inicio_residentes')
        else:
            form = CrearResidenteForm()
        return render(request, 'crear_residente.html', {'form': form})

    elif user.is_superuser == False or user.is_active == False:
        return redirect("home")
