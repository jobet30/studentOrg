from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            response_data = {
                'status': 'success',
                'message': 'User logged in successfully',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid credentials'
            }
            return JsonResponse(response_data, status=401)
    else:
        return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            response_data = {
                'status': 'success',
                'message': 'User registered successfully',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }
            return JsonResponse(response_data, status=201)
        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid form data',
                'errors': form.errors
            }
            return JsonResponse(response_data, status=400)
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@csrf_exempt
def user_profile(request):
    if request.method == 'GET':
        try:
            profile = get_object_or_404(Profile, user=request.user)
            response_data = {
                'username': profile.user.username,
                'bio': profile.bio,
                'profile_picture': profile.profile_picture.url if profile.profile_picture else None,
                'location': profile.location,
                'website': profile.website,
                'skills': [skill.name for skill in profile.user.skills.all()],
            }
            return JsonResponse(response_data, status=200)
        except Profile.DoesNotExist:
            response_data = {
                'status': 'error',
                'message': 'Profile not found'
            }
            return JsonResponse(response_data, status=404)

    return render(request, 'users/profile.html', {'profile': profile})

@csrf_exempt
def update_profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            response_data = {
                'status': 'success',
                'message': 'Profile updated successfully.',
            }
            return JsonResponse(response_data, status=200)
        else:
            response_data = {
                'status': 'error',
                'message': 'Invalid form data',
                'errors': form.errors
            }
            return JsonResponse(response_data, status=400)
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'users/update_profile.html', {'form': form})
