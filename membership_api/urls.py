from django.urls import path
from .views import SubscriptionPlanView,CardDetails,ListSubscriptionView,SubscriptionUpdate
from django.urls import include, re_path
from . import views
urlpatterns = [
    path('subscription-plan/',SubscriptionPlanView.as_view(), name='subscription-plan'),
 
    re_path(r'^test-payment/$', views.test_payment),
    re_path(r'^save-stripe-info/$', views.save_stripe_info),
    path('card-details/',CardDetails.as_view()),
    path('list-subscription-view/',ListSubscriptionView.as_view()),
    path('subscription-update/',SubscriptionUpdate.as_view()),
   
]