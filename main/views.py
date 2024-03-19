from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'title': 'Home',
        'content': 'Магазин строительных товаров OLI',
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'About us',
        'content': 'OLI - О нас',
        'text_on_page': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Non, eveniet?',
    }

    return render(request, 'main/about.html', context)
