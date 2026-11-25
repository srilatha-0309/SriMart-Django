
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Wishlist, Order
from django.db import transaction
from django.views.decorators.http import require_POST
from .models import Product, Cart, Wishlist, Order, OrderItem


def home(request):

    products = Product.objects.all()

    search_query = request.GET.get('search')

    if search_query:
        products = products.filter(
            name__icontains=search_query
        )

    else:
        products = products.filter(
            category__iexact='Non-Veg Pickles'
        )

    return render(request, 'store/home.html', {
        'products': products,
        'search_query': search_query
    })

    



@login_required(login_url='login')
def add_to_cart(request, product_id):

    if request.method == 'POST':

        product = get_object_or_404(Product, id=product_id)

        cart_item = Cart.objects.filter(
            user=request.user,
            product=product
        ).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()

        else:
            Cart.objects.create(
                user=request.user,
                product=product,
                quantity=1
            )

    return redirect('home')


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'store/register.html')


def login_user(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')

        else:
            messages.error(request, 'Invalid username or password!')

    return render(request, 'store/login.html')


@login_required(login_url='login')
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
@login_required(login_url='login')
def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')


@login_required(login_url='login')
def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        Cart,
        id=item_id,
        user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required(login_url='login')
def logout_user(request):

    logout(request)

    messages.success(request, 'Logout successful!')

    return redirect('login')
@login_required
def my_profile(request):

    return render(request, 'store/profile.html')
def category_products(request, category_name):

    products = Product.objects.filter(
        category__iexact=category_name
    )

    return render(request, 'store/category_products.html', {
        'products': products,
        'category_name': category_name
    })

@login_required(login_url='login')
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        wishlist_item.delete()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def my_wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product')

    return render(request, 'store/wishlist.html', {
        'wishlist_items': wishlist_items
    })
@login_required(login_url='login')
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'store/my_orders.html', {
        'orders': orders
    })
@login_required(login_url='login')
def checkout(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('product')

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required(login_url='login')
@require_POST
def place_order(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('product')

    if not cart_items.exists():
        messages.error(request, 'Your cart is empty!')
        return redirect('cart')

    full_name = request.POST.get('full_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    address = request.POST.get('address', '').strip()
    city = request.POST.get('city', '').strip()
    state = request.POST.get('state', '').strip()
    pincode = request.POST.get('pincode', '').strip()
    payment_method = request.POST.get('payment_method')

    if not all([full_name, phone, address, city, state, pincode]):
        messages.error(request, 'Please fill all delivery details.')
        return redirect('checkout')

    if not phone.isdigit() or len(phone) != 10:
        messages.error(request, 'Enter a valid 10-digit phone number.')
        return redirect('checkout')

    if not pincode.isdigit() or len(pincode) != 6:
        messages.error(request, 'Enter a valid 6-digit pincode.')
        return redirect('checkout')

    if payment_method != 'COD':
        messages.error(request, 'Invalid payment method.')
        return redirect('checkout')

    with transaction.atomic():

        cart_items = list(
            Cart.objects.filter(
                user=request.user
            ).select_related('product').select_for_update()
        )

        if not cart_items:
            messages.error(request, 'Your cart is empty!')
            return redirect('cart')

        total_price = 0

        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(
                    request,
                    f'Insufficient stock for {item.product.name}.'
                )
                return redirect('cart')

            total_price += item.product.price * item.quantity

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_amount=total_price,
            payment_method='COD'
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save(update_fields=['stock'])

        Cart.objects.filter(user=request.user).delete()

    return redirect('order_confirmation', order_id=order.id)

@login_required(login_url='login')
def order_confirmation(request, order_id):

    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user
    )

    return render(request, 'store/order_confirmation.html', {
        'order': order
    })

@login_required(login_url='login')
def track_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    status_order = [
        'Pending',
        'Confirmed',
        'Shipped',
        'Delivered'
    ]

    current_index = status_order.index(order.status) if order.status in status_order else -1

    status_steps = [
        {
            'name': 'Order Placed',
            'completed': current_index >= 0
        },
        {
            'name': 'Order Confirmed',
            'completed': current_index >= 1
        },
        {
            'name': 'Shipped',
            'completed': current_index >= 2
        },
        {
            'name': 'Delivered',
            'completed': current_index >= 3
        }
    ]

    return render(request, 'store/track_order.html', {
        'order': order,
        'status_steps': status_steps
    })

@login_required(login_url='login')
@require_POST

@login_required(login_url='login')
@require_POST
def cancel_order(request, order_id):

    with transaction.atomic():

        order = get_object_or_404(
            Order.objects.select_for_update(),
            id=order_id,
            user=request.user
        )

        if order.status == 'Pending':

            # Restore product stock
            order_items = order.items.select_related('product')

            for item in order_items:

                product = item.product

                product.stock += item.quantity

                product.save(update_fields=['stock'])

            # Update order status
            order.status = 'Cancelled'

            order.save(update_fields=['status'])

            messages.success(
                request,
                f'Order #{order.id} cancelled successfully! Stock restored.'
            )

        else:

            messages.error(
                request,
                'This order cannot be cancelled now.'
            )

    return redirect('my_orders')
    
