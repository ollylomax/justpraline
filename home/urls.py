from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]
