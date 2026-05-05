from django.contrib import admin
from django.urls import path
from inventory import views as inv_views  # Handles Books and Home Page
from accounts import views as acc_views   # Handles Users, Login, and Registration

urlpatterns = [
    # 1. Django Admin
    path('admin/', admin.site.urls),

    # 2. Page Rendering (Returns the HTML files)
    # These match the window.location.href redirects in your JavaScript
    path('', inv_views.home, name='home'),             # Your main dashboard
    path('register/', acc_views.register, name='register_page'), # Shows reg.html
    path('login/', acc_views.login, name='login_page'),       # Shows log.html

    # 3. Inventory API Endpoints (Pure Data)
    # Use these for Fetch calls in JS
    path('api/books/', inv_views.book_manager, name='book-manager'),
    path('api/books/<str:id>/', inv_views.book_detail, name='book-detail'),

    # 4. Accounts API Endpoints (Pure Data)
    # Use these for Fetch calls in JS
    path('api/register/', acc_views.register_user, name='api-register'),
    path('api/login/', acc_views.login_user, name='api-login'),
    path('api/users/all/', acc_views.get_all_users, name='all-users'),
]