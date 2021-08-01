from django.shortcuts import render
from mainapp.models import Product
from basketapp.models import Basket
from django.conf import settings
from django.core.cache import cache


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def main(request):
    products = get_products()[:2]

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
