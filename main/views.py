import re
from django.http import HttpResponse
from django.shortcuts import render
from goods.models import Categories

# Create your views here.
def index(request):

    categories = Categories.objects.all()

    context = {
        'title': 'Home',
        'content': 'Магазин строительных товаров OLI',
        'categories': categories,
        
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'О нас',
        'content': 'OLI - О нас',
        'text_on_page': 'Lorem ipsum dolor, sit amet consectetur adipisicing elit. Non, eveniet?',
    }

    return render(request, 'main/about.html', context)

def delivery(request):
    context = {
        'title' : 'Доставка и оплата',
        'content': 'Страница для указания оплаты и доставки',
        'text_on_page': 'Тут типо вводите данные все от карточек и свое местоположение',
    }

    return render(request, 'main/delivery.html', context)

def con_information(request):
    context = {
        'title': 'Content information',
        'content': 'Страница с контактной информацией',
        'text_on_page': 'Телефон: 88005553535 лучше позвони нам и купи какую-нибудь отвёртку',
    }

    return render(request, 'main/con_information.html', context)