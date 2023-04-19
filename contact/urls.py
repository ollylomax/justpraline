from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('edit/<int:message_id>/', views.edit_message, name='edit_message'),
    path(
        'delete/<int:message_id>/', views.delete_message, name='delete_message'),
]
