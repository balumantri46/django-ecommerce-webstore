from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from prdcatalog.models import Product
from .models import Cart, CartItem

def get_or_create_cart(request):
    cart_id = request.session.get('cart_id') # getting the session
    if cart_id:
        cart = Cart.objects.filter(cart_id=cart_id).first()
        if cart:
            return cart
    
    # Create new cart if not exists
    cart = Cart.objects.create()
    request.session['cart_id'] = cart.cart_id
    return cart

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        defaults={'cart_id': str(request.user.id)}
    )
    cart_items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.fn_price * item.quantity for item in cart_items)
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total,
        'cart': cart
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        messages.success(request, f'{product.name} added to cart successfully!')
    
    return redirect('prdlist')
@login_required
def remove_from_cart(request, product_id):
    # product = get_object_or_404(Product, id=product_id)
    # cart = get_or_create_cart(request)
    
    # # Find and delete the cart item
    # CartItem.objects.get(cart=cart, product=product).delete()
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    # cart = get_or_create_cart(request)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart.')
    return redirect('cart_detail')

@login_required
def update_cart_item(request, product_id):
    if request.method == 'POST':
        cart = Cart.objects.get(user=request.user)
        product = get_object_or_404(Product, id=product_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
            
    return redirect('cart_detail')
def success(request):
    return render(request, 'cart/sucess.html')

# Remove unused functions
# def clear_cart and def update_cart

# Create your views here.
