from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    def save(self,*args,**kwargs):
        if not self.slug: self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args,**kwargs)
    def __str__(self): return self.name
class Product(models.Model):
    title = models.CharField(max_length=180)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True)
    price = models.PositiveBigIntegerField(null=True, blank=True, help_text="قیمت به تومان؛ در صورت نامشخص بودن خالی بگذارید")
    image_url = models.URLField(blank=True)
    external_url = models.URLField(blank=True, help_text="لینک قانونی و مستقیم صفحه محصول در فروشگاه اصلی")
    store_name = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.title
class SellerApplication(models.Model):
    name = models.CharField(max_length=120)
    store_name = models.CharField(max_length=120)
    phone_or_email = models.CharField(max_length=160)
    website = models.URLField(blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    def __str__(self): return f"{self.store_name} - {self.name}"
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorited_by")
    class Meta: unique_together = ("user", "product")
    def __str__(self): return f"{self.user} - {self.product}"
