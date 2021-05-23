from django.shortcuts import render
from apps.product.models import Product

def home(request):
    newest_products = Product.objects.all()[0:8]
    return render(request, 'home.html', {'newest_products': newest_products})

def contact(request):
    return render(request, 'contact.html')
# Create your views here.
