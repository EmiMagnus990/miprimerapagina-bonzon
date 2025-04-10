from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from django.db import models
from django.contrib.auth.models import User

def index(request):
    return render(request, 'blog/index.html')

def post_list(request):
    post_list = Post.objects.all()
    return render(request, 'blog/post_list.html', context={"posts": post_list})

def manager_view(request):
    posts = Post.objects.all()
    return render(request, 'blog/manager.html', {'posts': posts})

def post_create(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        texto = request.POST['texto']
        fecha = timezone.now()
        Post.objects.create(titulo=titulo, texto=texto, fecha=fecha)
        return redirect('manager')
    return render(request, 'blog/create.html')

def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.titulo = request.POST['titulo']
        post.texto = request.POST['texto']
        post.save()
        return redirect('manager')
    return render(request, 'blog/update.html', {'post': post})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('manager')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect("index")
    return render(request, "blog/register.html")

@login_required
def profile_edit(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.username = form.cleaned_data.get('username')
            user.save()

            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
        })

    return render(request, 'blog/editar_perfil.html', {
        'profile_form': form
    })

@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    return render(request, 'blog/profile.html', {'profile': profile})

def about_view(request):
    return render(request, 'blog/about.html')