from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path(
        'delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('<int:product_id>/edit_product_review/<int:product_review_id>/', views.edit_product_review, name='edit_product_review'),
    path('<int:product_id>/delete_product_review/<int:product_review_id>/', views.delete_product_review, name='delete_product_review'),
]
