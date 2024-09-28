from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .cart import Cart
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse

def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'shop/category_detail.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'shop/product_detail.html', {'product': product})

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart_detail.html', {'cart': cart})

def cart_add(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity) 
    return redirect('cart_detail')

def cart_remove(request, slug):
    cart = Cart(request)
    product = get_object_or_404(Product, slug=slug)
    cart.remove(product)
    return redirect('cart_detail')

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

def checkout(request):
    cart = Cart(request)
    total_price = cart.get_total_price() * 100  # Stripe требует сумму в центах

    if request.method == 'POST':
        stripe_token = request.POST.get('stripeToken')

        # Проверка на наличие токена
        if not stripe_token:
            return render(request, 'shop/checkout_error.html', {'error': 'Ошибка: токен не был получен. Попробуйте еще раз.'})

        try:
            # Создаем платеж с использованием токена
            charge = stripe.Charge.create(
                amount=total_price,
                currency='usd',
                description='Товары из корзины',
                source=stripe_token,  # Используем полученный токен
            )
            cart.clear()  # Очищаем корзину после успешного платежа
            return render(request, 'shop/checkout_success.html')

        except stripe.error.StripeError as e:
            return render(request, 'shop/checkout_error.html', {'error': str(e)})
    
    return render(request, 'shop/checkout.html', {'total_price': total_price})