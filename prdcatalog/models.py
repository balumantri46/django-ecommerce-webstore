from django.db import models
class Category(models.Model):
    name = models.CharField(max_length=255,null=True,unique=True)
    def __str__(self) -> str:
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=20)
    desp = models.TextField(max_length=40)
    in_price = models.DecimalField(max_digits=20,decimal_places=2,default=20)
    fn_price = models.DecimalField(max_digits=20,decimal_places=2,default=0)
    brand = models.CharField(max_length=100,null=True)
    reviews = models.IntegerField(null=True)
    # img = models.ImageField(upload_to='prd_imgs/',blank=True, null=True) #for imgs from the local storage
    img = models.URLField(max_length=600,default='https://png.pngtree.com/png-vector/20221125/ourmid/pngtree-no-image-available-icon-flatvector-illustration-pic-design-profile-vector-png-image_40966566.jpg')
    published = models.DateField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   
    cat = models.ManyToManyField(Category,null=True,related_name='products') 
    def __str__(self) -> str:
        return self.name


# Create your models here.
