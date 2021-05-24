from django.contrib.auth.models import User
from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=225)
    joined_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='seller', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(seller_paid=False, order__sellers__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(seller_paid=True, order__sellers__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)

