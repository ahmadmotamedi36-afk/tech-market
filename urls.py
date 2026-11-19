from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from catalog import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),
    path("seller/apply/", views.seller_apply, name="seller_apply"),
    path("register/", views.register, name="register"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorite/<int:pk>/", views.toggle_favorite, name="toggle_favorite"),
    path("about/", views.about, name="about"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
