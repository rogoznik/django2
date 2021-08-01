import random

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.cache import cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


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


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = get_products()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]

    return same_products


def products(request, pk=None):
    print(pk)
    title = 'продукты'
    category = ''
    products = ''

    # categories = ProductCategory.objects.all()
    categories = get_links_menu()

    if pk is not None:
        if pk == 0:
            # products = Product.objects.all().order_by('price')
            products = get_products_orederd_by_price()
            category = {'name': 'все'}
        else:
            # category = get_object_or_404(ProductCategory, pk=pk)
            category = get_category(pk)
            products = get_products_in_category_orederd_by_price(pk)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'title': title,
        'categories': categories,
        'category': category,
        'products': products,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'products_list.html', context=context)


@login_required
def product(request, pk):
    title = 'страница продута'

    context = {
        'title': title,
        # 'categories': ProductCategory.objects.all(),
        'categories': get_links_menu(),
        # 'product': get_object_or_404(Product, pk=pk),
        'product': get_product(pk),
    }

    return render(request, 'product.html', context)
