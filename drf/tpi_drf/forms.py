from django import forms
from .models import Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Введите ваше сообщение...'}),
        }


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']