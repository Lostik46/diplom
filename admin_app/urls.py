from django.urls import path
from . import views

urlpatterns = [
    path('admin_home/', views.admin_home, name='admin_home'),
    path('search/', views.global_search, name='global_search'),
    path('add_product/', views.add_product, name='add_product'),  
    path('admin_products/', views.admin_products, name='admin_products'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin_clients/', views.admin_clients, name='admin_clients'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('update_order_status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('admin_news/', views.admin_news, name='admin_news'),
    path('admin/news/add/', views.add_news, name='add_news'),
    path('admin/news/edit/<int:news_id>/', views.edit_news, name='edit_news'),
    path('admin_reviews/', views.admin_reviews, name='admin_reviews'),
    path('publish-review/<int:review_id>/', views.publish_review, name='publish_review'),
    path('delete-review/<int:review_id>/', views.delete_review, name='delete_review'),
]