from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SellerApplication
class SellerApplicationForm(forms.ModelForm):
    class Meta:
        model=SellerApplication
        fields=["name","store_name","phone_or_email","website","message"]
        widgets={"message":forms.Textarea(attrs={"rows":4})}
class RegisterForm(UserCreationForm):
    email=forms.EmailField(required=False)
    class Meta:
        model=User
        fields=("username","email","password1","password2")
