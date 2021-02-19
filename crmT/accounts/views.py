from django.shortcuts import render
from .models import *


def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()
	total_orders = orders.count()
	orders_delivered = orders.filter(status='Delivered').count()
	orders_pending = orders.filter(status='Pending').count()

	context = {
		'customers': customers,
		'orders': orders,
		'total_orders': total_orders,
		'orders_delivered': orders_delivered,
		'orders_pending': orders_pending,
	}
	return render(request, 'accounts/dashboard.html', context)

def products(request):
	obj = Product.objects.all()
	context = {
		'products': obj
	}
	return render(request, 'accounts/products.html', context)

def customers(request, pk):
	def total_price(orders):
		t_price=0
		for order in orders:
			t_price = t_price + order.product.price
		return t_price
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	tot_price = total_price(orders) 
	context = {
		'customer': customer,
		'orders': orders,
		'tot_price':tot_price
		}
	return render(request, 'accounts/customers.html', context)
