from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order


def product_list(request):
    products = Product.objects.all()

    return render(
        request,
        'store/product_list.html',
        {'products': products}
    )


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(
        request,
        'store/product_detail.html',
        {'product': product}
    )


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})
    product_id = str(product.id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart

    return redirect('cart')


def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})
    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


def cart(request):
    cart_data = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(
        request,
        'store/cart.html',
        {
            'products': products,
            'total': total
        }
    )


def checkout(request):
    cart_data = request.session.get('cart', {})

    products = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total += subtotal

        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email')
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')

        Order.objects.create(
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            customer_address=customer_address,
            total_amount=total
        )

        request.session['cart'] = {}

        return render(request, 'store/order_success.html', {
            'customer_name': customer_name,
            'total': total
        })

    return render(request, 'store/checkout.html', {
        'products': products,
        'total': total
    })