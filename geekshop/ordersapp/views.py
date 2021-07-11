import json

from ordersapp.models import Order, OrderItem
from basketapp.models import Basket
from ordersapp.forms import OrderItemEditForm
from mainapp.models import Product

from django.urls.base import reverse
from django.forms.models import inlineformset_factory
from django.shortcuts import get_object_or_404, render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse


class OrderList(ListView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user, is_active=True)


class OrderCreate(CreateView):
    model = Order
    success_url = reverse_lazy('order:list')
    fields = []

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemEditForm,
            extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = list(Basket.objects.filter(user=self.request.user))
            if len(basket_items):
                OrderFormSet = inlineformset_factory(
                    Order,
                    OrderItem,
                    form=OrderItemEditForm,
                    extra=len(basket_items)
                )
                formset = OrderFormSet()

                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                    form.initial['price'] = basket_items[num].product.price
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderUpdate(UpdateView):
    model = Order
    success_url = reverse_lazy('order:list')
    fields = []

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(
            Order,
            OrderItem,
            form=OrderItemEditForm,
            extra=1
        )

        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset.forms:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price

        data['orderitems'] = formset

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            # form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')


class OrderRead(DetailView):
    model = Order


def forming_complite(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('order:list'))


def get_product_price(request, pk):
    data_response = {}

    if request.is_ajax():
        product = get_object_or_404(Product, pk=pk)
        data_response['price'] = str(product.price)

    return HttpResponse(json.dumps(data_response), content_type='application/json')
