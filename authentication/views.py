from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomPasswordResetForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            email = EmailMessage(
                'Welcome to Our Platform',
                'Thank you for registering.',
                to=[user.email]
            )
            email.send()
            return JsonResponse({'status': 'success', 'message': 'User registered successfully.'}, status=201)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    form = CustomUserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Logged in successfully.'}, status=200)
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'}, status=400)
    return render(request, 'authentication/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('authentication:login')

def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Password reset email sent.'}, status=200)
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    form = CustomPasswordResetForm()
    return render(request, 'authentication/password_reset.html', {'form': form})

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('authentication:profile')
        messages.error(request, 'Error updating profile.')
    else:
        form = CustomUserCreationForm(instance=request.user)
    return render(request, 'authentication/profile_update.html', {'form': form})
