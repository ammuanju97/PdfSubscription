
from .serializers import  SubscriptionPlanSerializer, CardSerializer, SubscriptionListSerializer

from .models import SubscriptionPlan, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.shortcuts import redirect
from membership.models import Customer
from rest_framework.decorators import api_view
import stripe
from membership.models import Customer, SubscriptionDetails
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.auth.models import User
from django.utils.timezone import make_aware
import datetime
from datetime import datetime

User = settings.AUTH_USER_MODEL



class SubscriptionPlanView(APIView):
    
    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response({"plans":serializer.data})
    

# stripe.api_key = 'sk_test_51LcLshSJSP7N6BFGjzRYCuYb2KbQlyZegzZgnKVjRYAs1Z3mHRQVFuKgK0Wk9kmeJXHpT9ZTwllZIpld0TyYLe2g00jGcYbhqF'   

@api_view(['POST'])
def test_payment(request):
    test_payment_intent = stripe.PaymentIntent.create(
        amount=1000, currency='pln', 
        payment_method_types=['card'],
        receipt_email='test@example.com')
    return Response(status=status.HTTP_200_OK, data=test_payment_intent)

# Create customer
@api_view(['POST'])
def save_stripe_info(request):
    data_value =  stripe.PaymentMethod.create(
    type="card",
    card={
        "number": "4242424242424242",
        "exp_month": 9,
        "exp_year": 2023,
        "cvc": "314",
    },
    )
    print(data_value)
    # data = request.data
    email = 'ol@gmail.com'
    payment_method_id = data_value.id
    print(payment_method_id)
    extra_msg = ''
    # checking if customer with provided email already exists
    customer_data = stripe.Customer.list(email=email).data
    print(customer_data)

    if len(customer_data) == 0:
        print('ooop')
        # creating customer
        customer = stripe.Customer.create(
            email=email,
            payment_method=payment_method_id,
            invoice_settings={
                'default_payment_method': payment_method_id
            }
        )
        print('koo')
        print(customer)
    else:
        print('helo')
        customer = customer_data[0]
        extra_msg = "Customer already existed."
       # creating paymentIntent
    # customer = stripe.Customer.create(
    #         email=email,
    #         payment_method=payment_method_id,
    #         invoice_settings={
    #             'default_payment_method': payment_method_id
    #         }
    #     )
    # print('koo')
    # print(customer)
    # stripe.PaymentIntent.create(customer=customer,
    #                             payment_method=payment_method_id,
    #                             currency='inr', amount=1500,
    #                             confirm=True)
    print('haii')
    
    stripe.Subscription.create(
    customer=customer,
    items=[
      {
       'price': 'price_1LrDXRSIfz0zIWXsePCsG9m8' #here paste your price id
      }
    ]
  )
      
    return Response('sucess')




class CardDetails(APIView):
    def post(self, request):
        serializer = CardSerializer(data = request.data)
        if serializer.is_valid():
            data_value =  stripe.PaymentMethod.create(
            type="card",
            card={
                "number":serializer.validated_data['number'],
                "exp_month": serializer.validated_data['exp_month'],
                "exp_year": serializer.validated_data['exp_year'],
                "cvc": serializer.validated_data['cvc'],
            },
            )
            
            email = serializer.validated_data['email']
            payment_method_id = data_value.id
            customer_data = stripe.Customer.list(email=email).data
           
            if len(customer_data) == 0:
                customer = stripe.Customer.create(
                    email=email,
                    payment_method=payment_method_id,
                    invoice_settings={
                        'default_payment_method': payment_method_id
                    }
                )
                # print(customer)
            else:
                customer = customer_data[0]
                extra_msg = "Customer already existed."
            subscription_details=stripe.Subscription.create(
                        customer=customer,
                        items=[
                        {
                        'price': 'price_1KsKWISDbesCS40HEcq6xBln' #here paste your price id
                        }
                        ]
                        )
            # print(subscription_details)
            #saving subscription details to customer and subscription details table
            user = User.objects.get(id=2)
            # print(user)
            new_customer = Customer.objects.create(
                # user = request.user,
                user=user,
                customer_id =customer.id,
                membership = True,
                cancel_at_period_end = False,
                stripe_subscription_id = subscription_details.id,
            )
            new_customer.save()
            
            # print(new_customer) 
            
            current_user = Customer.objects.get(user=user)
            print(current_user)
            # subscription_details = stripe.Subscription.retrieve(current_user.subscription)
            # print(subscription_details)
            # subscription_start_date = subscription_details.start_date
            subscription_start_date = subscription_details.current_period_start
            subscription_date = make_aware(datetime.fromtimestamp(subscription_start_date))
            print(subscription_date)
            
            print(subscription_details.plan['interval'])
            print(subscription_details.plan['amount'])
            subscription_end_date = subscription_details.current_period_end
            subscription_date_end = make_aware(datetime.fromtimestamp(subscription_end_date))
            list_details = Subscription_Details.objects.create(
                    user = user,
                    product_id=subscription_details.plan['product'],
                    subscription_status=subscription_details.status,
                    # subscription_type=subscription_details.plan['usage_type'],
                    subscription_amount=subscription_details.plan['amount']/100,
                    subscription_name=subscription_details.plan['interval'],
                    subscription_start_date = subscription_date,
                    subscription_end_date= subscription_date_end
                )
        
            list_details.save()      
    
            return Response('suceess',status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListSubscriptionView(APIView):
    def get(self, request):
        user = User.objects.get(id=2)
        details = SubscriptionDetails.objects.get(user=user)
        serializer = SubscriptionListSerializer(details)
        return Response({'details':serializer.data})
    

class SubscriptionUpdate(APIView):
    def get(self,request):
        user = User.objects.get(id=2)
        subscription =  stripe.Subscription.retrieve(user=user)
        subscription_update = stripe.Subscription.modify(
                    subscription.id,
                    items=[
                        {
                            'id': subscription['items']['data'][0].id,
            
                            'price': 'price_1KtUeSSDbesCS40H95RGMSIp',
                        }
                    ],
                )
        print(subscription_update)
        
        subscription_start_date = subscription_update.current_period_start
        subscription_date = make_aware(datetime.fromtimestamp(subscription_start_date))
        print(subscription_date)
        
        subscription_end_date = subscription_update.current_period_end
        subscription_date_end = make_aware(datetime.fromtimestamp(subscription_end_date))
        print(subscription_date_end)
        
        sub_update = SubscriptionDetails.objects.get(user =user)
        sub_update.subscription_amount = subscription_update.plan['amount']/100 
        sub_update.subscription_name = subscription_update.plan['interval']
        sub_update.subscription_start_date = subscription_date
        sub_update.subscription_end_date = subscription_date_end
        sub_update.save()        