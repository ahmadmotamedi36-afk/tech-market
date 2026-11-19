from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from .models import Product, Category, Favorite
from .forms import SellerApplicationForm, RegisterForm
def home(request):
    products=Product.objects.filter(is_active=True).select_related("category")
    q=request.GET.get("q","").strip(); category=request.GET.get("category",""); sort=request.GET.get("sort","new")
    if q: products=products.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(store_name__icontains=q))
    if category.isdigit(): products=products.filter(category_id=int(category))
    if sort=="cheap": products=products.order_by("price","-created_at")
    elif sort=="expensive": products=products.order_by("-price","-created_at")
    else: products=products.order_by("-created_at")
    fav_ids=set(Favorite.objects.filter(user=request.user).values_list("product_id",flat=True)) if request.user.is_authenticated else set()
    return render(request,"catalog/home.html",{"products":products,"categories":Category.objects.all(),"q":q,"selected_category":category,"sort":sort,"fav_ids":fav_ids})
def product_detail(request,pk):
    product=get_object_or_404(Product,pk=pk,is_active=True)
    is_fav=request.user.is_authenticated and Favorite.objects.filter(user=request.user,product=product).exists()
    return render(request,"catalog/product.html",{"product":product,"is_fav":is_fav})
def seller_apply(request):
    form=SellerApplicationForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): form.save(); messages.success(request,"درخواست شما ثبت شد. تیم TECH Market آن را بررسی می‌کند."); return redirect("seller_apply")
    return render(request,"catalog/seller.html",{"form":form})
def register(request):
    form=RegisterForm(request.POST or None)
    if request.method=="POST" and form.is_valid(): user=form.save(); login(request,user); messages.success(request,"حساب کاربری ساخته شد."); return redirect("home")
    return render(request,"catalog/register.html",{"form":form})
@login_required
@require_POST
def toggle_favorite(request,pk):
    product=get_object_or_404(Product,pk=pk,is_active=True)
    obj,created=Favorite.objects.get_or_create(user=request.user,product=product)
    if not created:
        obj.delete()
    return redirect(request.META.get("HTTP_REFERER") or "home")

def health(request):
    return HttpResponse("ok", content_type="text/plain")

def about(request):
    return render(request, "catalog/info.html", {"page_title":"درباره TECH Market", "body":"TECH Market بستری برای جست‌وجو و معرفی محصولات فروشگاه‌هاست. در مدل فعلی، خرید و پرداخت در وب‌سایت فروشنده انجام می‌شود."})

def privacy(request):
    return render(request, "catalog/info.html", {"page_title":"حریم خصوصی", "body":"این نسخه اطلاعات حساب کاربری و علاقه‌مندی‌ها را برای ارائه امکانات سایت ذخیره می‌کند. پیش از انتشار عمومی، متن این صفحه باید با شیوه واقعی جمع‌آوری، نگهداری و حذف داده‌ها و قوانین محل فعالیت تطبیق داده شود."})

def terms(request):
    return render(request, "catalog/info.html", {"page_title":"قوانین استفاده", "body":"TECH Market در نسخه فعلی محصولات را معرفی می‌کند و خرید در فروشگاه مقصد انجام می‌شود. قیمت، موجودی، شرایط ارسال و مرجوعی را پیش از خرید در وب‌سایت فروشنده بررسی کنید. مدیر سایت باید این متن را پیش از راه‌اندازی عمومی با شرایط واقعی کسب‌وکار تکمیل کند."})
@login_required
def favorites(request):
    products=Product.objects.filter(favorited_by__user=request.user,is_active=True).select_related("category")
    return render(request,"catalog/favorites.html",{"products":products,"fav_ids":set(products.values_list("id",flat=True))})
