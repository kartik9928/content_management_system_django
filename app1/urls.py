from django.urls import path
from app1 import views

urlpatterns = [
    path('start/', views.index , name='start'),
    path('insert/', views.UserCreation , name='insert'),
    path('insertBLog/', views.BlogCreations , name='blog'),
    path('login/', views.LoginUser , name='login'),
    path('getBlogs/', views.getBlogs , name='blogList'),
    path('search/', views.TagSearch , name='search'),
    path('findAutherBlog/', views.AutherBlog , name='findAutherBlog'),
    path('postComment/', views.postBlogComment , name='postComment'),
    path('getComment/', views.GetBlogComment , name='getComment'),
    path('GetAuthorBlogs/', views.GetAuthorBlogs , name='GetAuthorBlogs'),
]