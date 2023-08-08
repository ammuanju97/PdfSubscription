from django.contrib import admin

# Register your models here.
from .models import Product, SubscriptionPlan,CardDetails

admin.site.register(SubscriptionPlan)
admin.site.register(Product)
admin.site.register(CardDetails)