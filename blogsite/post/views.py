from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import PostForm
from .models import Post
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
import re


def home(request):
    posts = Post.objects.all().order_by('created_on')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})

def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/blog_detail.html', {'post': post})

@login_required
def manage_blogs(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('manage_blogs')
    else:
        form = PostForm()
    
    user_posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/manage_blogs.html', {'form': form, 'user_posts': user_posts})

@login_required
def edit_blog(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('manage_blogs')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_blog.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.errror(request, 'All fields are required.')
            return render(request, 'contact.html')

        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            messages.error(request, 'Invalid email address')
            return render(request, 'contact.html')
        try:
            send_mail(
                f'Message from {name}',
                message=message,
                from_email=settings.DEFAULT_FROM_MAIL,
                recipient_list=[settings.DEFAULT_TO_MAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            messages.error(request, f'Failed to send message: {str(e)}')

    return render(request, 'blog/contact.html')

def about(request):
    return render(request, 'blog/about.html')

@login_required
def profile(request):
    user = request.user
    return render(request, 'blog/profile.html', {'user': user})

@login_required
def setting(request):
    if request.method == "POST":
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        if request.POST.get('password'):
            user.set_password(request.POST['password'])
        user.save()
        return redirect('profile')  # Redirect after update

    return render(request, 'blog/setting.html')