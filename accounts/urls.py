from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('orders/', views.order_history, name='order_history'),
    path('past_order/<order_number>/', views.past_order, name='past_order'),
    path('messages/', views.message_centre, name='message_centre'),
    path(
        'past_message/<message_id>/', views.past_message, name='past_message'),
]
