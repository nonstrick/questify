from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm


def home(request):
    return render(request, 'home/index.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('profile')
    else:
        form = RegisterForm()
    
    return render(request, 'home/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('profile')
    else:
        form = LoginForm()
    
    return render(request, 'home/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('home')


@login_required
def profile_view(request):
    return render(request, 'home/profile.html', {'user': request.user})


def about_view(request):
    return render(request, 'home/about.html')


@login_required
def test_view(request):
    return render(request, 'home/test.html')


@login_required
def community_view(request):
    from django.contrib.auth.models import User
    from django.utils import timezone
    from datetime import timedelta
    
    total_users = User.objects.count()
    recent_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    users = User.objects.all().order_by('-date_joined')[:12]
    
    context = {
        'total_users': total_users,
        'recent_users': recent_users,
        'users': users,
    }
    
    return render(request, 'home/community.html', context)

