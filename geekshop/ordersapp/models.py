from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RD'
    CANCEL = 'CNC'
    DELEVERED = 'DVD'

    STATUSES = (
        (FORMING, 'формируется'),
        (SENT_TO_PROCEED, 'отправлен в обработку'),
        (PROCEEDED, 'обрабатывается'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (CANCEL, 'отменен'),
        (DELEVERED, 'выдан'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    create = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    update = models.DateTimeField(auto_now=True, verbose_name='обновлен')
    is_active = models.BooleanField(default=True)

    status = models.CharField(
        choices=STATUSES,
        default=FORMING,
        verbose_name='статус',
        max_length=3
    )

    def get_total_quantity(self):
        _items = self.orderitems.select_related()
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    def get_total_cost(self):
        _items = self.orderitems.select_related()
        _total_cost = sum(list(map(lambda x: x.get_product_cost(), _items)))
        return _total_cost

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItemQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for object in self:
            object.product.quantity += object.quantity
            object.product.save()
        super(OrderItemQuerySet, self).delete(*args, **kwargs)


class OrderItem(models.Model):
    objects = OrderItemQuerySet.as_manager()

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orderitems'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='продукт'
    )
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name='количество'
    )

    def get_product_cost(self):
        return self.product.price * self.quantity
