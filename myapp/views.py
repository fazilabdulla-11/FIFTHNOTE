from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Perfume, OrderItem
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def home(request):
    query = request.GET.get('q', '')
    perfumes = Perfume.objects.order_by('-created_at')

    if query:
        perfumes = perfumes.filter(
            name__icontains=query
        ) | perfumes.filter(
            brand__icontains=query
        )

    return render(request, 'home.html', {
        'perfumes': perfumes,
        'query': query,
    })


def perfume_detail(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    return render(request, 'detail.html', {'perfume': perfume})


def get_size_price(perfume, size):
    if size == '20ml':
        return perfume.price_20ml
    elif size == '50ml':
        return perfume.price_50ml
    return None


def add_to_cart(request, pk, size):
    perfume = get_object_or_404(Perfume, pk=pk)

    if size not in ['20ml', '50ml']:
        return redirect('myapp:detail', pk=pk)

    cart = request.session.get('cart', {})
    key = f'{pk}_{size}'

    cart[key] = cart.get(key, 0) + 1

    request.session['cart'] = cart
    return redirect('myapp:cart')


def cart(request):
    cart_data = request.session.get('cart', {})
    perfumes = []
    total = 0

    for key, quantity in cart_data.items():
        try:
            pk, size = key.rsplit('_', 1)
        except ValueError:
            continue

        perfume = get_object_or_404(Perfume, pk=pk)
        price = get_size_price(perfume, size)

        if price is None:
            continue

        item_total = price * quantity
        total += item_total

        perfumes.append({
            'perfume': perfume,
            'size': size,
            'price': price,
            'quantity': quantity,
            'item_total': item_total,
        })

    return render(request, 'cart.html', {
        'perfumes': perfumes,
        'total': total,
    })


def increase_cart(request, pk, size):
    cart_data = request.session.get('cart', {})
    key = f'{pk}_{size}'

    if key in cart_data:
        cart_data[key] += 1

    request.session['cart'] = cart_data
    return redirect('myapp:cart')


def decrease_cart(request, pk, size):
    cart_data = request.session.get('cart', {})
    key = f'{pk}_{size}'

    if key in cart_data:
        cart_data[key] -= 1

        if cart_data[key] <= 0:
            del cart_data[key]

    request.session['cart'] = cart_data
    return redirect('myapp:cart')


def remove_from_cart(request, pk, size):
    cart_data = request.session.get('cart', {})
    key = f'{pk}_{size}'

    if key in cart_data:
        del cart_data[key]

    request.session['cart'] = cart_data
    return redirect('myapp:cart')


def checkout(request):
    cart_data = request.session.get('cart', {})
    perfumes = []
    total = 0

    for key, quantity in cart_data.items():
        try:
            pk, size = key.rsplit('_', 1)
        except ValueError:
            continue

        perfume = get_object_or_404(Perfume, pk=pk)
        price = get_size_price(perfume, size)

        if price is None:
            continue

        item_total = price * quantity
        total += item_total

        perfumes.append({
            'perfume': perfume,
            'size': size,
            'price': price,
            'quantity': quantity,
            'item_total': item_total,
        })

    if request.method == 'POST' and perfumes:
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=name,
            phone=phone,
            address=address,
            pincode=pincode,
            total=total
        )

        for item in perfumes:
            OrderItem.objects.create(
                order=order,
                perfume=item['perfume'],
                size=item['size'],
                quantity=item['quantity'],
                price=item['price']
            )

        request.session['cart'] = {}

        return render(request, 'order_success.html')

    return render(request, 'checkout.html', {
        'perfumes': perfumes,
        'total': total,
    })


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        username = email

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'This email is already registered.'
            })

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        return redirect('myapp:login')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('myapp:home')

        return render(request, 'login.html', {
            'error': 'Invalid email or password'
        })

    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('myapp:home')


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('myapp:login')

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        'items__perfume'
    ).order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })

@login_required
@require_POST
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status == 'Pending':
        order.status = 'Cancelled'
        order.save(update_fields=['status'])

    return redirect('myapp:my_orders')

