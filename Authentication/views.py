from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import CustomUser, OTP
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, SetNewPasswordForm
from .utils import generate_otp, send_otp_email

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get('email')
            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            send_otp_email(user, otp)
            return redirect('verify_otp')
    else:
        form = CustomUserCreationForm()
    return render(request, 'Authentication/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if form.cleaned_data.get('remember_me'):
                request.session.set_expiry(1209600)  # Set session expiry to 2 weeks
            return redirect('profile')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'Authentication/login.html', {'form': form})

def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'Authentication/profile.html', {'form': form})

def request_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = CustomUser.objects.get(email=email)
            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            send_otp_email(user, otp)
            return redirect('verify_otp')
        except CustomUser.DoesNotExist:
            return redirect('request_otp')
    return render(request, 'Authentication/request_otp.html')

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = request.POST.get('otp')
        try:
            user = CustomUser.objects.get(email=email)
            otp_entry = OTP.objects.filter(user=user, otp=otp).latest('created_at')
            if otp_entry.is_expired():
                raise ValidationError('OTP has expired')
            user.email_verified = True
            user.save()
            login(request, user)
            otp_entry.delete()  # Remove OTP after successful verification
            return redirect('profile')
        except OTP.DoesNotExist:
            return redirect('verify_otp')
        except CustomUser.DoesNotExist:
            return redirect('verify_otp')
    return render(request, 'Authentication/verify_otp.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            OTP.objects.create(user=user, otp=otp)
            send_otp_email(user, otp)
            return redirect('reset_password')
        except User.DoesNotExist:
            return redirect('forgot_password')
    return render(request, 'Authentication/forgot_password.html')

def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect('reset_password')

        form = SetNewPasswordForm(user, request.POST)  # Pass user here
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            new_password = form.cleaned_data.get('new_password1')
            try:
                otp_entry = OTP.objects.filter(user=user, otp=otp).latest('created_at')
                if otp_entry.is_expired():
                    raise ValidationError('OTP has expired')
                user.set_password(new_password)
                user.save()
                otp_entry.delete()
                return redirect('login')
            except OTP.DoesNotExist:
                return redirect('reset_password')
    else:
        # Pass the user instance when rendering the form (this may not be necessary)
        form = SetNewPasswordForm(user=None)  # Initially, user is None since there's no POST data yet
    return render(request, 'Authentication/reset_password.html', {'form': form})