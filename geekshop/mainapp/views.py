import random

from django.shortcuts import render
from django.shortcuts import get_object_or_404

from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import login_required


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_products):
    same_products = Product.objects.filter(category=hot_products.category).exclude(pk=hot_products.pk)[:3]

    return same_products


def products(request, pk=None):
    print(pk)
    title = 'продукты'
    category = ''
    products = ''

    categories = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category_id__pk=pk).order_by('price')

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
        'categories': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'product.html', context)