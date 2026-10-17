from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def index(request):
    return render(request, 'landing/index.html')


def about(request):
    return render(request, 'landing/about.html')


def contact(request):
    return render(request, 'landing/contact.html')


def libros(request):
    return render(request,'landing/libros.html')


def categorias(request):
    return render(request,'landing/categorias.html')


def favoritos(request):
    return render(request,'landing/favoritos.html')


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('index')

    return render(request, 'usuarios/login.html')