from django.contrib import admin

from .models import Customer, SubscriptionDetails
# Register your models here.

admin.site.register(Customer)
admin.site.register(SubscriptionDetails)