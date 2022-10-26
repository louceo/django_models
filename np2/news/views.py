from .models import Post, Author, Category
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from datetime import datetime
from .filters import ProductFilter, CategoryFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import os


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        query_set = super().get_queryset()
        self.categoryfilter = CategoryFilter(self.request.GET, query_set)
        return self.categoryfilter.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['categoryfilter'] = self.categoryfilter
        if self.request.GET.get('category') and self.request.user.is_authenticated:
            context['is_not_subscribed'] = not Category.objects.filter(
                pk=self.request.GET.get('category'), subscribers__user=self.request.user).exists()
            context['category_name'] = Category.objects.get(
                pk=self.request.GET.get('category'))
            context['category_id'] = self.request.GET.get('category')
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        query_set = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, query_set)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetails(DetailView):
    model = Post
    template_name = 'detail.html'
    context_object_name = 'detail'


class PostCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    type = ''

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.type == 'PO':
            post.post_type = 'PO'
        else:
            post.post_type = 'AR'
        post.author = Author.objects.get(user=self.request.user.id)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        return context


class PostUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    type = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = self.type
        return context


class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news:news')


# @login_required
def subscribe_to_category(request, category_id):
    category = Category.objects.get(pk=category_id)
    author = Author.objects.get(user__username=request.user)
    if not Category.objects.filter(pk=category_id, subscribers__user=request.user).exists():
        category.subscribers.add(author.id)
    return redirect('news:news')
