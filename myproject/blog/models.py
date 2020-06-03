from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse


class Book(models.Model):
	isbn = models.CharField(max_length=100)
	title = models.CharField(max_length=100)
	authors = models.CharField(max_length=100)
	date_posted = models.DateTimeField(auto_now_add = True)
	update_date = models.DateTimeField(auto_now =True , blank= True )
	publication_date = models.DateField()
	# publication_date= forms.DateField(label='Publication date', widget=forms.SelectDateWidget)
	quantity = models.DecimalField(max_digits=3 , decimal_places=0)
	price = models.DecimalField(max_digits=6 , decimal_places=2)
	seller = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', kwargs={'pk' : self.pk})


	def get_update_cart_url(self):
		return reverse("update-cart", kwargs={'pk': self.pk})
	
	def get_delete_from_cart_url(self):
		return reverse("delete-cart", kwargs={'pk': self.pk})

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "{} of {}".format(self.quantity, self.item.title)

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total







