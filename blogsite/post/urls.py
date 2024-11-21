from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('manage-blogs/', views.manage_blogs, name='manage_blogs'),
    path('blog/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('blog/edit/<int:pk>/', views.edit_blog, name='edit_blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('setting/', views.setting, name='setting'),
]
