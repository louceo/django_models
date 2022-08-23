from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from datetime import datetime
# from pprint import pprint


class PostList(ListView):
    model = Post 
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetails(DetailView):
    model = Post
    template_name = 'detail.html' 
    context_object_name = 'details'
