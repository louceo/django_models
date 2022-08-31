from django.shortcuts import render, redirect
from .forms import UserForm
from django.views import generic
from django.contrib.auth.models import User, Group
from django.urls import reverse_lazy
from news.models import Author
from django.contrib.auth.decorators import login_required
from allauth.account.signals import user_signed_up
from django.dispatch import receiver


class UserRegistrationView(generic.CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('protect:profile')

    def form_valid(self, form):
        new_user = form.save()
        Author.objects.create(user=new_user)
        basic_group = Group.objects.get(name='authors')
        basic_group.user_set.add(new_user)
        return super().form_valid(form)


@login_required
def get_staff_access(request):
    user = request.user
    premium_group = Group.objects.get(name='staff')
    if not request.user.groups.filter(name='staff').exists():
        premium_group.user_set.add(user)
    return redirect('protect:profile')


@receiver(user_signed_up)
def after_user_signed_up(request, user, **kwargs):
    Author.objects.create(user=user)
    author_group = Group.objects.get(name='authors')
    author_group.user_set.add(user)
