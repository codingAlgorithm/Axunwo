from django import forms
from django.forms import ModelForm
from .models import RentPost

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(forms.Form):
    # use original html's form in signup.html, do not use django form related function, you don't need to add db operation in views.py
    pass

class PostForm(ModelForm):
        class Meta:
            model = RentPost
            exclude = ['user', 'post_time','photo_list',"post_sqft",'post_status',"post_bus","post_zipcode","post_subway"]


class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
    )