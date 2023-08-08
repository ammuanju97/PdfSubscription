from dataclasses import field
from pyexpat import model
from random import choices
from secrets import choice
from wsgiref import validate
from rest_framework import serializers
from .models import CardDetails, SubscriptionPlan


from membership.models import Customer, SubscriptionDetails


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
        
   

class CardSerializer(serializers.Serializer):
    number = serializers.IntegerField(help_text=u'The card number, as a string without any separators.', required=True)
    exp_month = serializers.IntegerField(help_text=u"Two digit number representing the card's expiration month.", required=True)
    exp_year = serializers.IntegerField(help_text=u"Two or four digit number representing the card's expiration year.", required=True)
    cvc = serializers.IntegerField(help_text=u'Card security code.', required=True)

    name = serializers.CharField(help_text=u"Cardholder's full name.", required=False, allow_null=True)
    email = serializers.EmailField(required=False, allow_null=True)
  
    
class SubscriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionDetails
        fields = ['subscription_status', 'subscription_amount','subscription_name','subscription_start_date','subscription_end_date']
        
        
