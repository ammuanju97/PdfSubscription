from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views import generic
from .forms import CustomSignupForm
from .models import Customer, SubscriptionDetails
import stripe
from django.conf import settings


stripe.api_key = "sk_test_51LrDTvSIfz0zIWXsrgtOvYlVpeMKjY4vmvK5YeOSoaBbuiTSFzivjK8q1EfoWNsHpoCTXkyyGiGqglmIZvmzdgoP00FJ41wAnd"

def home_page(request):
    return render(request, 'membership/home.html')


def join_page(request):
    return render(request, 'membership/join.html')


def cancel_page(request):
    return render(request, 'membership/cancel.html')


class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


@login_required
def checkout(request):

    # try:
      
    #     return redirect('settings')
    # except Customer.DoesNotExist:
    #     pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 100
        membership_id = 'price_1MgiMDSIfz0zIWXsQHtxeXh8'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1MgiMDSIfz0zIWXs77v7XKJj'
                final_dollar = 1200

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',

            cancel_url='http://127.0.0.1:8000/cancel',
        )
        print(session)
        return render(request, 'membership/checkout.html', {'session_id': session.id, 'final_dollar': final_dollar})


def success_page(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        print('ahh')
        print(session)
        print(session.subscription)
        customer = Customer.objects.create(
                user = request.user,
                customer_id = session.customer,
                membership= True,
                cancel_at_period_end = False,
                stripe_subscription_id = session.subscription,
            )
        customer.save()
        
        current_user = Customer.objects.get(user=request.user)
        subscription_details = stripe.Subscription.retrieve(session.subscription)
        print(subscription_details)
        # subscription_start_date = subscription_details.start_date
        subscription_start_date = subscription_details.current_period_start
        subscription_date = make_aware(datetime.fromtimestamp(subscription_start_date))
        print(subscription_date)
        
        print(subscription_details.plan['interval'])
        print(subscription_details.plan['amount'])
        subscription_end_date = subscription_details.current_period_end
        subscription_date_end = make_aware(datetime.fromtimestamp(subscription_end_date))
        list_details = SubscriptionDetails.objects.create(
                user = request.user,
                product_id=subscription_details.plan['product'],
                subscription_status=subscription_details.status,
                # subscription_type=subscription_details.plan['usage_type'],
                subscription_amount=subscription_details.plan['amount']/100,
                subscription_name=subscription_details.plan['interval'],
                subscription_start_date = subscription_date,
                subscription_end_date= subscription_date_end
            )
        
        list_details.save()
        print(list_details)
    return render(request, 'membership/success.html')


@login_required
def settings_page(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        pass
        # try:
        #     if request.user.customer.membership:
        #         membership = True
        #     if request.user.customer.cancel_at_period_end:
        #         cancel_at_period_end = True
        # except Customer.DoesNotExist:
        #     membership = False
    return render(request, 'registration/settings.html', {'membership':membership,
                    'cancel_at_period_end':cancel_at_period_end})
   
    
def list_subscription(request):
    if request.method=='GET':
        try:
            data ={}
            current_user = Customer.objects.get(user=request.user)
            print(current_user)
            list_details = SubscriptionDetails.objects.get(user=request.user)
            print(list_details)
            data['status'] = list_details.subscription_status 
            data['trial_start'] = list_details.subscription_start_date
            data['trial_end'] = list_details.subscription_end_date
            data['amount'] = list_details.subscription_amount
            data['name'] =  list_details.subscription_name
            # data['remaining_days'] = u.remaining_days
           
            return render(request, 'membership/list.html',{'data':data})
        except:
            return HttpResponse(' no active subscription ')
        
        
def update_subscription(request):
    if request.method == 'GET':
        subscription =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription_update = stripe.Subscription.modify(
                    subscription.id,
                    items=[
                        {
                            'id': subscription['items']['data'][0].id,
            
                            'price': 'price_1LrJGOSIfz0zIWXsRRcdT49C',
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
        
        sub_update = SubscriptionDetails.objects.get(user = request.user)
        sub_update.subscription_amount = subscription_update.plan['amount']/100 
        sub_update.subscription_name = subscription_update.plan['interval']
        sub_update.subscription_start_date = subscription_date
        sub_update.subscription_end_date = subscription_date_end
        sub_update.save()        
        return render(request,'membership/update.html')
    
    
# def pause_subscription(request):
#     coustomer_id = stripe.Subscription.retrieve(
#         request.user.customer.stripe_subscription_id),
#     stripe.Subscription.modify(
        
#         request.user.customer.stripe_subscription_id,
#         pause_collection={
#             'behavior': 'mark_uncollectible',
#         },
#     )
#     # return HttpResponse("Successfully paused")
#     return render(request, 'membership/pause.html')


# #resume a subscription
# def resume_subscription(request):
#     coustomer_id = stripe.Subscription.retrieve(
#         request.user.customer.stripe_subscription_id),
#     stripe.Subscription.modify(
#         request.user.customer.stripe_subscription_id,
#         pause_collection='',
#     )
#     # return HttpResponse("Resumed")
#     return render(request, 'membership/resume.html')
