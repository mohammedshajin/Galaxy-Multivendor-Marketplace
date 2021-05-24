from django.shortcuts import redirect, render ,get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from apps.product.models import Product  
from.models import Seller
from.forms import ProductForm, ProductImageForm

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
    orders = seller.orders.all()

    for order in orders:
        order.seller_amount = 0
        order.seller_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.seller == request.user.seller:
                if item.seller_paid:
                    order.seller_paid_amount += item.get_total_price()
                else:
                    order.seller_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'seller_admin.html', {'seller': seller, 'products': products, 'orders': orders})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller
            product.slug = slugify(product.title)
            product.save()

            return redirect('seller_admin')
    else:
        form = ProductForm()
    
    return render(request, 'add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    seller = request.user.seller
    product = seller.products.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            productimage = image_form.save(commit=False)
            productimage.product = product
            productimage.save()

            return redirect('seller_admin')

        if form.is_valid():
            form.save()

            return redirect('seller_admin')
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm()
    
    return render(request, 'edit_product.html', {'form': form, 'image_form': image_form, 'product': product})

@login_required
def edit_seller(request):
    seller = request.user.seller

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            seller.created_by.email = email
            seller.created_by.save()

            seller.name = name
            seller.save()

            return redirect('seller_admin')
    
    return render(request, 'edit_seller.html', {'seller': seller})


def sellers(request):
    sellers = Seller.objects.all()

    return render(request, 'sellers.html', {'sellers': sellers})

def seller(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)

    return render(request, 'seller.html', {'seller': seller})
