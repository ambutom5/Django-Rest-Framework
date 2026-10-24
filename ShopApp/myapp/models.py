from django.db import models

# Create your models here.

class CategoryDb(models.Model):
    category_name = models.CharField()
    description = models.TextField()

    def __str__(self):
        return self.category_name

class ProductDb(models.Model):
    category = models.ForeignKey(CategoryDb,on_delete=models.CASCADE)
    product_name = models.CharField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return self.product_name
    

