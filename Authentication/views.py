from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import CustomUser, OTP
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .utils import generate_otp, send_otp_email
from django.contrib.auth.tokens import default_token_generator

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
            # Handle user not found
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
            user.is_active = True
            user.save()
            login(request, user)
            otp_entry.delete()  # Remove OTP after successful verification
            return redirect('profile')
        except OTP.DoesNotExist:
            # Handle invalid OTP
            return redirect('verify_otp')
        except CustomUser.DoesNotExist:
            # Handle user not found
            return redirect('verify_otp')
    return render(request, 'Authentication/verify_otp.html')
