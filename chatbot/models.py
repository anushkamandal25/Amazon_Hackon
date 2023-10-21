from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=1000, null=True)
    name= models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    price = models.CharField(max_length=200,null=False, blank=False)
    description = models.TextField(max_length=500, null=True)
    rating = models.CharField(max_length=50, null=True)
    rating_count = models.CharField(max_length=200,null=True)
    image_link = models.CharField(max_length=500, null=True)
    product_link = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
