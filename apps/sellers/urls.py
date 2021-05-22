from django.urls import path
from.import views

urlpatterns = [
    path('become-seller/', views.become_seller,name='become_seller'),
    
]