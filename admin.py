from django.contrib import admin
from .models import Category, Product, SellerApplication, Favorite
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin): list_display=("name","slug"); prepopulated_fields={"slug":("name",)}
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin): list_display=("title","category","price","store_name","is_active"); list_filter=("category","is_active"); search_fields=("title","description","store_name"); list_editable=("is_active",)
@admin.register(SellerApplication)
class SellerApplicationAdmin(admin.ModelAdmin): list_display=("store_name","name","phone_or_email","created_at","reviewed"); list_filter=("reviewed",); search_fields=("store_name","name","phone_or_email")
admin.site.register(Favorite)
admin.site.site_header = "مدیریت TECH Market"
admin.site.site_title = "TECH Market Admin"
admin.site.index_title = "مدیریت فروشگاه و محصولات"
