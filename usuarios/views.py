from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse
from .models import PasswordResetCode
import random


def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)

            return redirect('index')


        else:

            messages.error(
                request,
                "Usuario o contraseña incorrectos"
            )


    return render(
        request,
        'usuarios/login.html'
    )



def register(request):

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']


        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "El usuario ya existe"
            )

            return redirect('register')


        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        user.save()


        messages.success(
            request,
            "Usuario creado correctamente"
        )


        return redirect('login')


    return render(
        request,
        'usuarios/register.html'
    )

def forgot_password(request):

    if request.method == "POST":

        username = request.POST['username']

        try:

            user = User.objects.get(
                username=username
            )

            code = str(
                random.randint(
                    100000,
                    999999
                )
            )
            
            PasswordResetCode.objects.filter(
                user=user
            ).delete()
            
            PasswordResetCode.objects.create(
                user=user,
                code=code
            )

            request.session['reset_user'] = user.id

            html_content = render_to_string(
                'emails/recovery_email.html',
                {
                    'username': user.username,
                    'code': code,
                }
            )

            email = EmailMultiAlternatives(
                subject='Recuperación de contraseña - Biblioteca Virtual',
                body='Tu cliente de correo no soporta mensajes HTML.',
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
            )

            email.attach_alternative(
                html_content,
                "text/html"
            )

            email.send()

            messages.success(
                request,
                "Se ha enviado un código de recuperación a tu correo electrónico."
            )

            return redirect('verify_code')

        except User.DoesNotExist:

            messages.error(
                request,
                "El usuario no existe"
            )

    return render(
        request,
        'usuarios/forgot_password.html'
    )

def verify_code(request):

    if request.method == "POST":

        code = request.POST['code']

        user_id = request.session.get('reset_user')

        if user_id:

            reset_code = PasswordResetCode.objects.filter(
                user_id=user_id,
                code=code,
                used=False
            ).last()

            if reset_code:

                request.session['verified_reset'] = True

                reset_code.used = True
                reset_code.save()

                return redirect('change_password')

            else:

                messages.error(
                    request,
                    "Código incorrecto"
                )

        else:

            messages.error(
                request,
                "La sesión de recuperación ha expirado."
            )

            return redirect('forgot_password')

    return render(
        request,
        'usuarios/verify_code.html'
    )

def change_password(request):

    if not request.session.get('verified_reset'):

        return redirect('forgot_password')


    if request.method == "POST":

        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:

            messages.error(
                request,
                "Las contraseñas no coinciden."
            )

            return redirect('change_password')


        user = User.objects.get(
            id=request.session['reset_user']
        )

        user.set_password(password)
        user.save()


        request.session.pop('reset_user', None)
        request.session.pop('verified_reset', None)


        messages.success(
            request,
            "Contraseña actualizada correctamente."
        )

        return redirect('login')


    return render(
        request,
        'usuarios/change_password.html'
    )

def logout_view(request):

    logout(request)

    return redirect('login')

def test_email(request):

    send_mail(
        subject='Prueba Biblioteca Virtual',
        message='¡Hola! Este correo fue enviado correctamente desde Django.',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
        fail_silently=False
    )

    return HttpResponse("Correo enviado correctamente.")