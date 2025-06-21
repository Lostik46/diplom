from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import include, path
from django.conf.urls.static import static
from . import settings
from admin_app import views

urlpatterns = [
    path('', include('client_app.urls')), 
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls), 
    path('meneger/', include('admin_app.urls')), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)