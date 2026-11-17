from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['full_name'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'John Doe'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'name@example.com'
        })
        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '+1 (555) 000-0000'
        })
        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a strong password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Repeat your password'
        })


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email Address'
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'name@example.com'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'phone', 'avatar', 'bio']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+1 (555) 000-0000'
            }),
            'avatar': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a short bio about yourself as a contributor...'
            })
        }
