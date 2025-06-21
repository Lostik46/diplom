import json
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from . import models
from django.shortcuts import  get_object_or_404, render, redirect
from . import forms
from . import models
from django.contrib.auth import  login
from client_app import forms as cf
from admin_app import forms as af
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.db.models import Q
from .models import Product, Client, Orders, News, Review
from django.contrib.auth.models import User
from .models import Client, Orders, Review
from django.urls import reverse 

def global_search(request):
    query = request.GET.get('query', '')  # Получаем поисковый запрос
    results = []

    if query:
        # Поиск по модели Product
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(short_description__icontains=query)
        ).distinct()
        for product in products:
            results.append({
                'table': 'Продукты',
                'result': f"{product.name} (Категория: {product.category.category_name})",
                'url': reverse('edit_product', args=[product.id]),  # Ссылка на редактирование продукта
                'details': f"Цена: {product.price} руб., Описание: {product.short_description}"  # Дополнительная информация
            })

        # Поиск по модели Client
        clients = Client.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(email__icontains=query)
        ).distinct()
        for client in clients:
            results.append({
                'table': 'Клиенты',
                'result': f"{client.first_name} {client.last_name} (Телефон: {client.mobile})",
                'url': f"{reverse('admin_clients')}?highlight={client.id}",  # Ссылка на страницу клиентов
                'details': f"Email: {client.email}, Адрес: {client.address}"  # Дополнительная информация
            })

        # Поиск по модели Orders
        orders = Orders.objects.filter(
            Q(client__first_name__icontains=query) |
            Q(client__last_name__icontains=query) |
            Q(product__name__icontains=query) |
            Q(email__icontains=query) |
            Q(address__icontains=query) |
            Q(mobile__icontains=query)
        ).distinct()
        for order in orders:
            results.append({
                'table': 'Заказы',
                'result': f"Заказ #{order.id} от {order.client.first_name} {order.client.last_name}",
                'url': f"{reverse('admin_orders')}?highlight={order.id}",  # Ссылка на страницу заказов
                'details': f"Товар: {order.product.name}, Статус: {order.status}"  # Дополнительная информация
            })

        # Поиск по модели News
        news = News.objects.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(short_text__icontains=query)
        ).distinct()
        for item in news:
            results.append({
                'table': 'Новости',
                'result': f"{item.title} (Дата публикации: {item.publish_date})",
                'url': reverse('edit_news', args=[item.id]),  # Ссылка на редактирование новости
                'details': f"Краткое описание: {item.short_text}"  # Дополнительная информация
            })

        # Поиск по модели Review
        reviews = Review.objects.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(product__name__icontains=query) |
            Q(text__icontains=query)
        ).distinct()
        for review in reviews:
            results.append({
                'table': 'Отзывы',
                'result': f"Отзыв от {review.user.first_name} {review.user.last_name} на {review.product.name if review.product else 'магазин'}",
                'url': f"{reverse('admin_reviews')}?highlight={review.id}",  # Ссылка на страницу отзывов
                'details': f"Рейтинг: {review.rating}, Текст: {review.text[:100]}..."  # Дополнительная информация
            })

        # Поиск по модели auth_user (стандартная модель User)
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()
        for user in users:
            # Проверяем, существует ли клиент для этого пользователя
            try:
                client = Client.objects.get(user=user)
                results.append({
                    'table': 'Пользователи',
                    'result': f"{user.username} (Имя: {user.first_name} {user.last_name}, Email: {user.email})",
                    'url': f"{reverse('admin_clients')}?highlight={client.id}",  # Ссылка на страницу клиентов
                    'details': f"Телефон: {client.mobile}, Адрес: {client.address}"  # Дополнительная информация
                })
            except Client.DoesNotExist:
                results.append({
                    'table': 'Пользователи',
                    'result': f"{user.username} (Имя: {user.first_name} {user.last_name}, Email: {user.email})",
                    'url': reverse('admin_clients'),  # Ссылка на страницу клиентов
                    'details': "Клиент не зарегистрирован"  # Дополнительная информация
                })

    return render(request, 'admin_app/search_results.html', {'results': results, 'query': query})

def login_view(request):
    if request.method == 'POST':
        form = cf.LoginForm(request.POST)
        if form.is_valid():
            user = form.user
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home') 
            return redirect('home') 
    else:
        form = cf.LoginForm()
    return render(request, 'login.html', {'form': form})

def admin_home(request):
    # Количество клиентов, заказов и отзывов
    total_clients = Client.objects.count()
    total_orders = Orders.objects.count()
    total_reviews = Review.objects.count()

    # Статистика по заказам (например, за последние 7 дней)
    from datetime import timedelta
    from django.utils import timezone

    last_7_days = timezone.now() - timedelta(days=7)
    orders_last_7_days = Orders.objects.filter(order_date__gte=last_7_days).count()

    # Статистика по отзывам (например, за последние 7 дней)
    reviews_last_7_days = Review.objects.filter(created_at__gte=last_7_days).count()

    # Статистика по новым регистрациям (например, за последние 7 дней)
    new_clients_last_7_days = Client.objects.filter(user__date_joined__gte=last_7_days).count()

    return render(request, 'admin_app/admin_home.html', {
        'total_clients': total_clients,
        'total_orders': total_orders,
        'total_reviews': total_reviews,
        'orders_last_7_days': orders_last_7_days,
        'reviews_last_7_days': reviews_last_7_days,
        'new_clients_last_7_days': new_clients_last_7_days,
    })

def admin_products(request):
    query = request.GET.get('query', '')  # Получаем поисковый запрос
    products = models.Product.objects.all()
    products_category = models.ProductCategory.objects.all()

    if query:
        # Фильтруем продукты по запросу
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__category_name__icontains=query) |
            Q(price__icontains=query) |
            Q(short_description__icontains=query) |
            Q(quantity__icontains=query) |
            Q(volume__icontains=query) |
            Q(discount__icontains=query)
        )

    return render(request, 'admin_app/admin_products.html', {
        'products': products,
        'products_category': products_category,
        'query': query  # Передаем запрос в шаблон
    })

def edit_product(request, product_id):
    product = get_object_or_404(models.Product, id=product_id)
    if request.method == 'POST':
        form = af.ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
    else:
        form = af.ProductForm(instance=product)
    return render(request, 'admin_app/edit_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = models.Product.objects.get(id=product_id)
    product.delete()
    return redirect('admin_products')

def add_product(request):
    if request.method == 'POST':
        form = af.ProductForm(request.POST, request.FILES)  # Создаем форму с данными из запроса
        if form.is_valid():
            form.save()  # Сохраняем новый продукт
            return redirect('admin_products')  # Перенаправляем на список продуктов
    else:
        form = af.ProductForm()  # Пустая форма для создания продукта
    return render(request, 'admin_app/add_product.html', {'form': form})

def admin_clients(request):
    clients = models.Client.objects.all()
    highlight_id = request.GET.get('highlight')  # Получаем идентификатор для подсветки
    return render(request, 'admin_app/admin_clients.html', {
        'clients': clients,
        'highlight_id': highlight_id  # Передаем идентификатор в шаблон
    })

def admin_orders(request):
    orders = models.Orders.objects.all().order_by('-id')
    return render(request, 'admin_app/admin_orders.html', {'orders': orders})

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(models.Orders, id=order_id)
        new_status = request.POST.get('status')

        if new_status in dict(models.Orders.STATUS).keys():
            order.status = new_status
            order.save()
            messages.success(request, 'Статус заказа успешно обновлен.')
        else:
            messages.error(request, 'Неверный статус.')

    return redirect('admin_orders')

def admin_news(request):
    news = models.News.objects.all().order_by('-publish_date')
    return render(request, 'admin_app/admin_news.html', {'news': news})

def add_news(request):
    if request.method == 'POST':
        form = forms.NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_news') 
    else:
        form = forms.NewsForm() 
    return render(request, 'admin_app/add_news.html', {'form': form})

def edit_news(request, news_id):
    news = get_object_or_404(models.News, id=news_id)
    if request.method == 'POST':
        form = forms.NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('admin_news')  
    else:
        form = forms.NewsForm(instance=news) 
    return render(request, 'admin_app/edit_news.html', {'form': form, 'news': news})

def admin_reviews(request):
    reviews = models.Review.objects.all()
    highlight_id = request.GET.get('highlight')  # Получаем идентификатор для подсветки
    return render(request, 'admin_app/admin_reviews.html', {
        'reviews': reviews,
        'highlight_id': highlight_id  # Передаем идентификатор в шаблон
    })

@csrf_exempt
def publish_review(request, review_id):
    if request.method == 'POST':
        try:
            review = models.Review.objects.get(id=review_id)
            review.published = True
            review.save()
            messages.success(request, 'Отзыв успешно опубликован.')
        except models.Review.DoesNotExist:
            messages.error(request, 'Отзыв не найден.')
    return redirect('admin_reviews')  # Перенаправляем обратно на страницу отзывов

@csrf_exempt
def delete_review(request, review_id):
    if request.method == 'POST':
        try:
            review = models.Review.objects.get(id=review_id)
            review.delete()
            messages.success(request, 'Отзыв успешно удален.')
        except models.Review.DoesNotExist:
            messages.error(request, 'Отзыв не найден.')
    return redirect('admin_reviews')  # Перенаправляем обратно на страницу отзывов
