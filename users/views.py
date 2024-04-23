from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title': 'OLI - Авторизация'
    }
    return render(request, 'users/login.html', context)

def registration(request):
    context = {
        'title': 'OLI - Регистрация'
    }
    return render(request, 'users/registration.html', context)

def profile(request):
    context = {
        'title': 'OLI - Профиль'
    }
    return render(request, 'users/profile.html', context)

def logout(request):
    ...
