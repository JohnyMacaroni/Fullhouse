from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

'''
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']'''





class TransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    price = forms.DecimalField(max_digits=10, decimal_places=2, required=True)