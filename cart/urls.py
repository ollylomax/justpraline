from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<item_id>/', views.add_to_cart, name='add_to_cart'),
    path('amend/<item_id>/', views.quantity_amend, name='quantity_amend'),
    path('delete/<item_id>/', views.delete_from_cart, name='delete_from_cart'),
]
