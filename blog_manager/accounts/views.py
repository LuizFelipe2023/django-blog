from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import RegisterForm, CustomLoginForm, ProfileUpdateForm
from .models import CustomUser


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome to NewsBlog, {user.full_name or user.email}! Your account was created successfully.')
            return redirect('news_home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name or user.email}! You are now logged in.')
            return redirect('news_home')
    else:
        form = CustomLoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully. See you soon!')
    return redirect('news_home')


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    user_news = request.user.news.prefetch_related('images').order_by('-id')
    return render(request, 'accounts/profile.html', {
        'user_news': user_news,
        'profile_form': form,
    })


# --- Views Administrativas ---

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(is_admin, login_url='news_home')
def admin_users_list(request):
    users = CustomUser.objects.all().order_by('-id')
    return render(request, 'accounts/admin_users.html', {'users': users})


@user_passes_test(is_admin, login_url='news_home')
def admin_toggle_staff(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            messages.error(request, 'You cannot remove your own admin privileges.')
        else:
            target_user.is_staff = not target_user.is_staff
            target_user.save()
            messages.success(request, f'Permissions updated for {target_user.full_name}.')
    return redirect('admin_users_list')


@user_passes_test(is_admin, login_url='news_home')
def admin_toggle_active(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            messages.error(request, 'You cannot deactivate your own account.')
        else:
            target_user.is_active = not target_user.is_active
            target_user.save()
            messages.success(request, f'Status updated for {target_user.full_name}.')
    return redirect('admin_users_list')


@user_passes_test(is_admin, login_url='news_home')
def admin_user_delete(request, user_id):
    if request.method == 'POST':
        target_user = get_object_or_404(CustomUser, id=user_id)
        if target_user == request.user:
            messages.error(request, 'You cannot delete your own account here.')
        else:
            name = target_user.full_name
            target_user.delete()
            messages.success(request, f'User {name} has been deleted.')
    return redirect('admin_users_list')
