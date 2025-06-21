from django.urls import path
from django.contrib.auth.views import LoginView,LogoutView
from . import views  

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('product/<int:id>/', views.product_detail, name='product-detail'),
    path('signup/', views.client_signup_view, name='signup'),
    path('catalog/', views.catalog, name='catalog'),
    path('about_us/', views.about_us, name='about_us'),
    path('news/', views.news, name='news'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('reviews/', views.reviews, name='reviews'),
]
