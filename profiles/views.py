from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm

@login_required
def profile_detail(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'user_profiles/profile_detail.html', {'profile': profile})

@login_required
def profile_update(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profiles:profile_detail')
    else:
        form = ProfileUpdateForm(instance=profile)
    return render(request, 'user_profiles/profile_update.html', {'form': form})