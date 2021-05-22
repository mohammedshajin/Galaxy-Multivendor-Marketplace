from django.contrib.auth import views as auth_views
from django.urls import path
from.import views

urlpatterns = [
    path('become-seller/', views.become_seller, name='become_seller'),
    path('seller-admin/', views.seller_admin, name='seller_admin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   
]