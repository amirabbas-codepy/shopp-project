
from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput())
    phone_number = forms.CharField(max_length=11, min_length=11, required=True)
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=True)
    adress = forms.CharField(widget=forms.Textarea(), required=True)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput())

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(), required=True)

class SerchForm(forms.Form):
    value = forms.CharField(max_length=200)

class EditAdressForm(forms.Form):
    adr = forms.CharField(required=True, widget=forms.Textarea(), label='ادرس جدید')