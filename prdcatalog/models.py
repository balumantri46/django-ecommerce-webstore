from django.db import models
class Product(models.Model):
    name = models.CharField(max_length=20)
    desp = models.TextField(max_length=40)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    img = models.ImageField(upload_to='prd_imgs/',blank=True)
    published = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


# Create your models here.
