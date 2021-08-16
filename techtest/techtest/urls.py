"""techtest URL Configuration

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
from django.contrib import admin
from django.urls import path
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.index, name='index'),
    path(r'', views.index, name='home'),
    path('home/product/', views.product, name='products.html'),
    path('home/cart/', views.cart, name='cart'),
    path('home/checkout/', views.checkout, name='checkout'),
    path('api/initiatePayment/', views.initiatePayment, name='payment'),
    path('api/redirect/', views.initiatePayment, name='payment.html'),
    path('result/success', views.success, name='success'),
    path('result/error', views.error, name='error'),
    path('result/pending', views.pending, name='pending'),
    path('home/add/<int:pid>/', views.add_toCart, name='add_toCart'),
    path('home/remove/<int:pid>/', views.remove_fromCart, name='remove_fromCart'),
    path('home/clear-cart/', views.clear_cart, name='clear-cart'),
]
