
from .models import FinanceEntry
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm


class FinanceEntryForm(forms.ModelForm):
    class Meta:
        model = FinanceEntry
        fields = ['entry_type', 'amount', 'category', 'date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class signupForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
