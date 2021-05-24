from django.contrib.auth import views as auth_views
from django.urls import path
from.import views

urlpatterns = [
    path('become-seller/', views.become_seller, name='become_seller'),
    path('seller-admin/', views.seller_admin, name='seller_admin'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_seller/', views.edit_seller, name='edit_seller'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', views.sellers, name='sellers'),
    path('<int:seller_id>', views.seller, name='seller'),
   
]