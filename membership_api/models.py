from pyexpat import model
from statistics import mode

from django.db import models

# Create your models here.
PLAN_NAME = (
    ("monthly",'monthly'),
     ("yearly",'yearly')
)

PLAN_PRICE = (
    ("100","100"),
    ("1200","1200")
)

class SubscriptionPlan(models.Model):
    plan_name = models.CharField(max_length = 20,choices = PLAN_NAME)
    plan_price = models.CharField(max_length = 20,choices = PLAN_PRICE)
    
    def __str__(self):
        return self.plan_name
    

class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    # product_image=models.ImageField(upload_to="thumbnail")
    # book_url=models.URLField()
    def __str__(self):
        return self.name


class CardDetails(models.Model):
    
    number = models.CharField(max_length=100)
    exp_month = models.CharField(max_length=100)
    exp_year = models.CharField(max_length=100)
    cvc = models.CharField(max_length=100)

    name = models.CharField(max_length=100)
    
    
