from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile_number', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'mobile_number']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']
