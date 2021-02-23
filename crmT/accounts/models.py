from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=50, null=True)
	phone = models.CharField(max_length=20, null=True)
	email = models.EmailField(max_length=100, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return '%s' % self.name


class Tag(models.Model):
	name = models.CharField(max_length=100, null=True)
	def __str__(self):
		return '%s' % self.name


class Product(models.Model):
	CATEGORY = (
		('Indoor', 'Indoor'),
		('Out Door', 'Out Door')
		)
	name = models.CharField(max_length=100, null=True)
	price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	category = models.CharField(max_length=100, null=True, choices=CATEGORY)
	description = models.TextField(max_length=500, null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	tags = models.ManyToManyField(Tag)

	def __str__(self):
		return '%s' % self.name


class Order(models.Model):
	STATUS = (
		('Pending', 'Pending'),
		('Out for delivery', 'Out for delivery'),
		('Delivered', 'Delivered')
		)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True) 
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)  
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	status = models.CharField(max_length=100, null=True, choices=STATUS)

	def __str__(self):
		return '%s' % self.product.name