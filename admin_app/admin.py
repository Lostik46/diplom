from django.contrib import admin
from .models import ProductCategory, Product, Client, Cart, News, Review, Orders

class ClientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Client, ClientAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'short_description')    
admin.site.register(ProductCategory, ProductCategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class OrdersAdmin(admin.ModelAdmin):
    pass
admin.site.register(Orders, OrdersAdmin)

class ReviewAdmin(admin.ModelAdmin):
    pass
admin.site.register(Review, ReviewAdmin)

class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percentage')
