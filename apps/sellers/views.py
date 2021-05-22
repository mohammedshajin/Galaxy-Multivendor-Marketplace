from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from apps.product.models import Product  
from.models import Seller

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

# Create your views here.
