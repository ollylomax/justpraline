from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_cache/', views.checkout_cache, name='checkout_cache'),
    path('checked_out/<order_number>/', views.checked_out, name='checked_out'),
    path('webhook/', webhook, name='webhook'),
]
