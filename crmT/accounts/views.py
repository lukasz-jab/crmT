from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm

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

def createOrder(request):
	form = OrderForm()
	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
		else:
			raise ValueError("Błędne dane")
			form = OrderForm()
	context={
		'form': form
	}
	return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
		else:
			raise ValueError("Błędne dane")
			form = OrderForm(instance=order)
	context={
		'form': form
	}
	return render(request, 'accounts/order_form.html', context)		

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {
		'item': order
	}
	return render(request, 'accounts/delete.html', context)


