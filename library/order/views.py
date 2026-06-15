from django.shortcuts import render
from .models import Order

def order_list(request):
    orders = Order.get_all()
    return render(request, 'order/order_list.html', {'orders': orders})