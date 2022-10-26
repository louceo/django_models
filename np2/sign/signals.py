from news.models import Author
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from allauth.account.signals import user_signed_up
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os


@receiver(user_signed_up)
def after_user_signed_up(request, user, **kwargs):
    Author.objects.create(user=user)
    author_group = Group.objects.get(name='authors')
    author_group.user_set.add(user)

    # html_content = render_to_string('signed_up.html', {'user': user})

    msg = EmailMultiAlternatives(subject=f'Welcome aboard, {user.username}!', body='Thank you for registering on Music Scope!', from_email=os.environ.get(
        'EMAIL_CRED')+'@yandex.ru', to=[user.email, ])
    msg.send()
