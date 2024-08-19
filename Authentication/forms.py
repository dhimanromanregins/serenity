from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import CustomUser
from django.contrib.auth.forms import SetPasswordForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile_number', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'mobile_number', 'address', 'date_of_birth', 'first_name', 'last_name', 'profile_photo', 'bio']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ['old_password', 'new_password1', 'new_password2']


class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)

class SetNewPasswordForm(SetPasswordForm):
    otp = forms.CharField(max_length=6, required=True)
    email = forms.EmailField(max_length=254, required=True)

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
