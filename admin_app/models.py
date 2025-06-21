from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import phonenumbers
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_russian_mobile(value):
    try:
        # Удаляем все нецифровые символы для проверки
        digits = ''.join(filter(str.isdigit, value))
        if not digits.startswith('7') or len(digits) != 11:
            raise ValidationError("Номер должен начинаться с +7 и содержать 11 цифр")
        
        phone = phonenumbers.parse('+' + digits)
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Номер телефона недействителен")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Неверный формат номера телефона")
        phone = phonenumbers.parse(value, "RU")
        if not phonenumbers.is_valid_number(phone):
            raise ValidationError("Номер телефона недействителен.")
    except phonenumbers.phonenumberutil.NumberParseException:
        raise ValidationError("Неверный формат номера телефона.")

cyrillic_validator = RegexValidator(
    regex='^[а-яА-ЯёЁ\s]+$', 
)

class ProductCategory(models.Model):
    category_name = models.CharField(max_length=250)
    short_description = models.CharField(max_length = 250, default='краткое описание')

    def __str__(self):
        return self.category_name

class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=250, verbose_name='Название')
    product_image = models.ImageField(
        upload_to='product_image/',
        null=True,
        blank=True,
        default='product_image/default_product_image.jpg',
        verbose_name='Изображение'
    )
    price = models.PositiveIntegerField(verbose_name='Цена')
    description = models.CharField(max_length=900, verbose_name='Описание')
    short_description = models.CharField(max_length = 250, default='краткое описание', verbose_name='Краткое описание')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    volume = models.PositiveIntegerField(default=100, verbose_name='Объём')
    is_on_sale = models.BooleanField(default=False,verbose_name='Акция (да/нет)')  
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Размер скидки') 
    created_at = models.DateTimeField(default=datetime.now, verbose_name='Дата создания')

    def __str__(self):
        return self.name
    
    @property
    def sale_price(self):
        if self.is_on_sale and self.discount:
            return self.price * (1 - self.discount / 100)
        return self.price

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Псевдоним')
    first_name = models.CharField(max_length=250, validators=[cyrillic_validator], verbose_name='Имя')
    last_name = models.CharField(max_length=250, validators=[cyrillic_validator], verbose_name='Фамилия')
    mobile = models.CharField(max_length=18, null=False, validators=[validate_russian_mobile], 
                             verbose_name='Мобильный телефон')  # Изменили длину на 18
    # остальные поля без изменений

    mobile = models.CharField(max_length=11, null=False, validators=[validate_russian_mobile], verbose_name='Мобильный телефон')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='Электронная почта')
    address = models.CharField(max_length=40, null=True, blank=True, verbose_name='Адрес')

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 
    
    def get_name(self):
        return f"{self.first_name} {self.last_name}"


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Cart item: {self.product.name} (Quantity: {self.quantity}) for {self.client.first_name} {self.client.last_name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

class Orders(models.Model):
    STATUS = (
        ('Ожидается', 'Ожидается'),
        ('Подтвержден', 'Подтвержден'),
        ('В пути', 'В пути'),
        ('Доставлен', 'Доставлен'),
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField(default=0)  # Добавляем поле количества
    email = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=500, null=True)
    mobile = models.CharField(max_length=20, null=True)
    order_date = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=50, null=True, choices=STATUS)

    def __str__(self):
        return f"Order #{self.id} by {self.client.get_name}"

class News(models.Model):
    title = models.CharField(max_length=255)
    img = models.ImageField(
        upload_to='news_img/',
        null=True,
        default='news_img/default_image.jpg'
    )
    text = models.TextField()  
    short_text = models.TextField()  
    publish_date = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.title
    
class Review(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    text = models.TextField() 
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) 
    created_at = models.DateTimeField(auto_now_add=True) 
    published = models.BooleanField(default=False)

    def __str__(self):
        return f"Отзыв от {self.user.user} на {self.product.name if self.product else 'магазин'}"