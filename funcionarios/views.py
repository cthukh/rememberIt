from django.shortcuts import render,redirect

# Create your views here.


def inicio(request):
    if not request.user.is_authenticated:
        return redirect("funcionario:registro")
    return render(request,"inicio.html")



def registro(request):
    return render(request,"iniciarses.html")