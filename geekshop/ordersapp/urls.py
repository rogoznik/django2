from django.urls import path
import ordersapp.views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderList.as_view(), name='list'),
    path('create/', ordersapp.OrderCreate.as_view(), name='create'),
    path('update/<pk>/', ordersapp.OrderUpdate.as_view(), name='update'),
    path('delete/<pk>/', ordersapp.OrderDelete.as_view(), name='delete'),
    path('read/<pk>/', ordersapp.OrderRead.as_view(), name='read'),
    path(
        'forming/complete/<pk>',
        ordersapp.forming_complite,
        name='forming_complite'
    ),
]