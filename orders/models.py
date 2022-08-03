from itertools import product
from django.db import models
from store.models import Product,Variation
from accounts.models import Account
# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id
class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled')   ,
    )
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    order_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(models.Model)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=140)
    address_line_2 = models.CharField(max_length=140,blank=True)
    country = models.CharField(max_length=50)
    state  = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=60)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation,on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.product_name






