from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Products, CartItemsz
from django.http import HttpResponse
from django.contrib.auth import login
from .forms import SignUpForm


def index(request):
    products = Products.objects.all()
    return render(request, 'index.html', {'products': products})

def detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    return render(request, 'detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    
    cart_item, created = CartItemsz.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItemsz.objects.filter(user=request.user)
    return render(request, 'cart.html', {'cart_items': cart_items})

@login_required
def delete_from_cart(request, item_id):
    item = get_object_or_404(CartItemsz, id=item_id, user=request.user)
    item.delete()
    return redirect('cart_view')
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user after registration
            return redirect('index')  # Redirect to a successful registration page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})