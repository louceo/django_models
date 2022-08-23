from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

class PostList(ListView):
    model = Post 
    template_name = 'news.html'
    context_object_name = 'news'

class PostDetails(DetailView):
    model = Post
    template_name = 'detail.html' 
    context_object_name = 'details'