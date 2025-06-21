import json
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from admin_app import models
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from . import forms
from django.utils.safestring import mark_safe
<<<<<<< HEAD
import logging
logger = logging.getLogger(__name__)
=======
>>>>>>> 75f9f11385247bda242880355abcf51ee6601242

def client_signup_view(request):
    userForm = forms.ClientUserForm()
    clientForm = forms.ClientForm()
    mydict = {'userForm': userForm, 'ClientForm': clientForm}
<<<<<<< HEAD
    
    if request.method == 'POST':
        userForm = forms.ClientUserForm(request.POST)
        clientForm = forms.ClientForm(request.POST, request.FILES)
        
        if userForm.is_valid() and clientForm.is_valid():
            try:
                user = userForm.save(commit=False)
                user.set_password(user.password)
                user.save()
                
                customer = clientForm.save(commit=False)
                customer.user = user
                customer.save()
                
                messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти в систему.")
                return redirect('login')
                
            except Exception as e:
                if getattr(user, 'pk', None):
                    user.delete()
                messages.error(request, "Произошла непредвиденная ошибка при регистрации. Пожалуйста, попробуйте позже.")
                logger.error(f"Registration error: {str(e)}", exc_info=True)
                
        else:
            # Обработка ошибок формы пользователя
            if 'username' in userForm.errors:
                messages.error(request, "Псевдоним уже занят или содержит недопустимые символы. Пожалуйста, выберите другой.")
            if 'password' in userForm.errors:
                messages.error(request, "Пароль слишком простой или не соответствует требованиям безопасности.")
            
            # Обработка ошибок формы клиента
            if 'first_name' in clientForm.errors:
                messages.error(request, "Имя должно содержать только русские буквы и начинаться с заглавной буквы.")
            if 'last_name' in clientForm.errors:
                messages.error(request, "Фамилия должна содержать только русские буквы и начинаться с заглавной буквы.")
            if 'mobile' in clientForm.errors:
                messages.error(request, "Введите корректный российский номер телефона (например: 79123456789).")
            if 'email' in clientForm.errors:
                messages.error(request, "Введите корректный адрес электронной почты (например: example@mail.ru).")
    
=======
    if request.method == 'POST':
        userForm = forms.ClientUserForm(request.POST)
        clientForm = forms.ClientForm(request.POST, request.FILES)
        if userForm.is_valid() and clientForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customer = clientForm.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти.")
            return redirect('login') 
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
>>>>>>> 75f9f11385247bda242880355abcf51ee6601242
    return render(request, 'client_app/sign_up.html', context=mydict)

def home_view(request):
    products = models.Product.objects.order_by('-created_at')[:4]
    sale_products = models.Product.objects.filter(is_on_sale=True)

    context = {
        'products': products,
        'sale_products': sale_products,
        'product_count_in_cart': 0, 
    }

    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter = product_ids.split('|')
        context['product_count_in_cart'] = len(set(counter))

    return render(request, 'client_app/index.html', context) 

def product_detail(request, id):
    product = get_object_or_404(models.Product, id=id)
    return render(request, 'client_app/product_detail.html', {'product': product})

def catalog(request):
    products = models.Product.objects.all()
    query = request.GET.get('search')
    if query:
        products = products.filter(name__icontains=query)
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    categories = models.ProductCategory.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'query': query, 
    }

    return render(request, 'client_app/catalog.html', context)

def about_us(request):
    return render(request, 'client_app/about_us.html')

def news(request):
    news = models.News.objects.all().order_by('-publish_date')
    return render(request, 'client_app/news.html', {'news': news})

def add_to_cart(request, pk):
    product = get_object_or_404(models.Product, id=pk)
    client = models.Client.objects.get(user=request.user)

    cart_item, created = models.Cart.objects.get_or_create(
        client=client,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        if cart_item.quantity < product.quantity:
            cart_item.quantity += 1 
            cart_item.save()
        else:
            messages.warning(request, f"В наличии только {product.quantity} единиц товара '{product.name}'. Максимально добавлено в корзину: {product.quantity}.")
            cart_item.quantity = product.quantity
            cart_item.save()

    return redirect('product-detail', id=product.id)

def cart(request):
    product = models.Product.objects.all()
    cart_items = models.Cart.objects.filter(client=request.user.client)
    total_cart_price = sum(item.total_price for item in cart_items)
    return render(request, 'client_app/cart.html', {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'product' : product,
    })

def update_cart(request, item_id):
    item = get_object_or_404(models.Cart, id=item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > item.product.quantity:
            messages.error(request, f"Недостаточно товара на складе. Максимальное количество: {item.product.quantity}")
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, "Количество товара обновлено.")
    return redirect('cart')

def remove_from_cart(request, item_id):
    item = models.Cart.objects.get(id=item_id)
    item.delete()
    return redirect('cart')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправляем на страницу входа, если пользователь не авторизован

    client = request.user.client
    cart_items = models.Cart.objects.filter(client=client)

    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')  # Получаем список выбранных товаров

        # Проверяем, выбраны ли товары
        if not selected_items:
            messages.error(request, "Выберите хотя бы один товар для оформления заказа.")
            return redirect('checkout')  # Перенаправляем обратно на страницу оформления заказа

        email = request.POST.get('email', client.email)
        mobile = request.POST.get('mobile', client.mobile)
        address = request.POST.get('address', client.address)

        # Создаем заказ для каждого выбранного товара
        for item_id in selected_items:
            cart_item = models.Cart.objects.get(id=item_id)
            order = models.Orders(
                client=client,
                product=cart_item.product,
                quantity=cart_item.quantity,
                email=email,
                mobile=mobile,
                address=address,
                status='Ожидается оплата'  # Новый статус заказа
            )
            order.save()

            # Удаляем товар из корзины
            cart_item.delete()

        # Перенаправляем на страницу фиктивной оплаты
        return redirect('order_confirmation')

    return render(request, 'client_app/checkout.html', {
        'cart_items': cart_items,
        'client': client,
    })

def order_confirmation(request):
    if request.method == 'POST':
        orders = models.Orders.objects.filter(client=request.user.client, status='Ожидается оплата')

        for order in orders:
            if order.quantity > order.product.quantity:
                return redirect('order_confirmation')

        for order in orders:
            order.product.quantity -= order.quantity
            order.product.save()
            order.status = 'Подтвержден'
            order.save()

        return redirect('profile') 

    return render(request, 'client_app/order_confirmation.html')

@login_required
def profile(request):
    client = request.user.client  # Получаем объект Client для текущего пользователя
    orders = models.Orders.objects.filter(client=client).order_by('-order_date')  # Получаем заказы пользователя
    return render(request, 'client_app/profile.html', {
        'client': client,
        'orders': orders,
    })

@login_required
def edit_profile(request):
    client = request.user.client  # Получаем объект Client для текущего пользователя

    if request.method == 'POST':
        form = forms.ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль успешно обновлен.")
            return redirect('profile')
    else:
        form = forms.ClientForm(instance=client)

    return render(request, 'client_app/edit_profile.html', {
        'form': form,
    })

@login_required
def reviews(request):
    client = request.user.client
    user_orders = models.Orders.objects.filter(client=client)
    reviews = models.Review.objects.filter(published=True).order_by('-created_at')

    # Добавляем поле rating_stars для каждого отзыва
    for review in reviews:
        review.rating_stars = '★' * review.rating

    if request.method == 'POST':
        product_id = request.POST.get('product')
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        if not product_id:
            messages.error(request, "Выберите товар для отзыва.")
            return redirect('reviews')

        product = models.Product.objects.get(id=product_id)

        models.Review.objects.create(
            user=client,
            product=product,
            text=text,
            rating=rating,
            published=False
        )
        messages.success(request, "Ваш отзыв отправлен на модерацию.")
        return redirect('reviews')

    return render(request, 'client_app/reviews.html', {
        'user_orders': user_orders,
        'reviews': reviews,
    })