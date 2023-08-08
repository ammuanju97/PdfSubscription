"""pdfmembership URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from membership import views

urlpatterns = [
    path('membership/', include('membership.urls')),
    path('membership_api/',include('membership_api.urls')),
  
    path('', views.home_page, name='home'),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/signup/', views.SignUp.as_view(), name='signup'),
    path('auth/settings/', views.settings_page, name='settings'),
    path('join/', views.join_page, name='join'),
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_page, name='success'),
    path('cancel/', views.cancel_page, name='cancel'),

    path('update-subscription/',views.update_subscription,name='updatesubscription'),
    # path('pause-subscription/',views.pause_subscription,name='pausesubscription'),
    # path('resume-subscription/',views.resume_subscription,name='resumesubscription'),
    path('list-subscription/',views.list_subscription, name='listsubscription'),
    # path('updateaccounts', views.updateaccounts, name='updateaccounts'),
]
