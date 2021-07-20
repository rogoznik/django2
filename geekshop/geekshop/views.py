from django.shortcuts import render
from mainapp.models import Product
from basketapp.models import Basket


def main(request):
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:2]

    basket = ''
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    context = {
        'slogan': 'Супер пупер СТУЛЬЯ',
        'topic': 'Тренды',
        'title': 'главная',
        'products': products,
        'basket': basket,
    }
    return render(request, 'index.html', context=context)


def contacts(request):
    context = {
        'title': 'контакты',
    }
    return render(request, 'contact.html', context=context)
