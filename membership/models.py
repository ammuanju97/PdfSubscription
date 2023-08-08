
from django.db import models
from django.contrib.auth.models import User




class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_username')
    customer_id = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    
class SubscriptionDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription_username')
    product_id = models.CharField(max_length=100)
    subscription_status = models.CharField(max_length=20)
    subscription_amount = models.IntegerField()
    subscription_name = models.CharField(max_length=100)
    subscription_start_date = models.DateTimeField()
    subscription_end_date = models.DateTimeField()
    
    def __str__(self):
        return self.user.username
    
    # @property
    # def remaining_days(self):
    #     remaining = (datetime.datetime.now().date() - self.subscription_end_date.date()).days
    #     u=Subscription_Details.objects.all().first()
    #     u.remaining_days  
    

        