from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from .forms import ProfileUpdateForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def Register(request):
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
            profile = Profile.objects.get(user=request.user)
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
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Profile not found'}, status=404)

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
