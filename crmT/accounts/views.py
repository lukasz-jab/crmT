from django.shortcuts import render, redirect
from .models import *
from .forms import OrderForm, FormUserCreation
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
from .decorators import unauthenticated_user, allowed_users, admin_only

@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(['admin'])
def products(request):
	obj = Product.objects.all()
	context = {
		'products': obj
	}
	return render(request, 'accounts/products.html', context)


@login_required(login_url='login')
@allowed_users(['admin'])
def customers(request, pk):
	def total_price(orders):
		t_price=0
		for order in orders:
			t_price = t_price + order.product.price
		return t_price
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()
	tot_price = total_price(orders) 

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs
	
	context = {
		'customer': customer,
		'orders': orders,
		'tot_price': tot_price,
		'myFilter': myFilter,
		}
	return render(request, 'accounts/customers.html', context)


@login_required(login_url='login')
@allowed_users(['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),
		extra=7)
	customer = Customer.objects.get(id=pk)
	#form = OrderForm(initial={'customer': customer})
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	if request.method == 'POST':
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')
		else:
			raise ValueError("Błędne dane")
			form = OrderForm()
	context={
		'formset': formset,
		'customer': customer,
	}
	return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(['admin'])
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


@login_required(login_url='login')
@allowed_users(['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == 'POST':
		order.delete()
		return redirect('/')
	context = {
		'item': order
	}
	return render(request, 'accounts/delete.html', context)


def registerPage(request):
	form = FormUserCreation()
	if request.method == 'POST':
		form = FormUserCreation(request.POST)
		if form.is_valid():
			user = form.save()
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			messages.success(request, 'Acount was created successful for ' + form.cleaned_data.get('username'))
			return redirect('login')

	context = {
		'form': form 
	}
	return render(request, 'accounts/register.html', context)


def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Sorry, we couldn\'t find an account with this username:  ' + username + 
							' or the password was not valid, please try recover (or Sign Up) your username' )

	context = {

	}
	return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
def userPage(request):
	
	context = {

	}
	return render(request, 'accounts/user.html', context)
