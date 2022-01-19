"""restaurant URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django import urls
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from django.conf.urls.static import static
import restaurant.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('delivery', views.delivery, name='delivery'),
    path('preorder', views.preorder, name='preorder'),
    path('download_preorder', views.download_preorder, name='download_preorder'),
    path('create_order', views.create_order, name='create_order'),
    path('reservation', views.reservation, name='reservation'),
    path('feedback', views.feedback, name='feedback'),
    path('events', views.events, name='events'),
    path('career', views.career, name='career'),
    path('franchise', views.franchise, name='franchise'),
    path('contacts', views.contacts, name='contacts'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('recovery', views.recovery, name='recovery'),
    path('personal', views.personal, name='personal'),
    path('cabinet', views.cabinet, name='cabinet'),
    path('restaraunts', views.restaraunts, name='restaraunts'),
    path('captcha', views.captcha, name='captcha'),

    path('set_city_id', views.set_city_id, name='set_city_id'),

    path('payment_success', views.payment_success, name='payment_success'),
    path('payment_fail', views.payment_fail, name='payment_fail'),

    path('pclogin', views.pclogin, name='pclogin'),
    path('pcbooking', views.pcbooking, name='pcbooking'),
    path('pcdelivery', views.pcdelivery, name='pcdelivery'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
