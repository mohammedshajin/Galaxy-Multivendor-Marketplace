from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from apps.product.models import Product  
from.models import Seller
from.forms import ProductForm

def become_seller(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user =form.save()

            login(request, user)

            seller = Seller.objects.create(name=user.username, created_by=user)
        return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'become_seller.html', {'form': form})

@login_required
def seller_admin(request):
    seller = request.user.seller
    products = seller.products.all()
    return render(request, 'seller_admin.html', {'seller': seller, 'products':products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})
