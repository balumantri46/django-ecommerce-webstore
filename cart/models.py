from django.db import models
from prdcatalog.models import Product
from django.contrib.auth.models import User
# from django.contrib.auth.decorators import property
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return str(self.cart_id)
    #property is used as a geter that gets the total of the cart when called by Cart.total
    @property
    def total(self):
        cart_items = self.cartitem_set.all()
        return sum(item.subtotal for item in cart_items)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    #property is used as a geter that gets the subtotal of the cart item when called by CartItem.subtotal
    @property 
    def subtotal(self):
        return self.quantity * self.product.fn_price

# Create your models here.
