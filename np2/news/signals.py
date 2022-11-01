from .models import Post, Category
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os
import datetime
from .tasks import notify_subscribers_async
from django.conf import settings


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, **kwargs):
    categories = instance.category.all()
    merged = []
    for category in categories:
        emails = list(category.subscribers.all(
        ).values_list('user__email', flat=True))
        merged += emails
    cleaned_emails = list(set(merged))
    html_content = render_to_string('notify_subs.html', {'post': instance})
    sub = instance.header
    msg = instance.content[:124]
    from_email = settings.EMAIL_HOST_USER
    notify_subscribers_async.delay(
        html_content, sub, msg, cleaned_emails, from_email)
