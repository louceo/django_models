from .models import Post, Category
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import os
import datetime


@receiver(m2m_changed, sender=Post.category.through)
def notify_subscribers(sender, instance, **kwargs):
    categories = list(instance.category.all().values_list('id', flat=True))
    merged = []
    for category in categories:
        emails = list(Category.objects.filter(pk=category).values_list(
            'subscribers__user__email', flat=True))
        merged += emails
    cleaned_emails = list(set(merged))
    html_content = render_to_string('notify_subs.html', {'post': instance})

    msg = EmailMultiAlternatives(subject=instance.header, body=instance.content[:124], from_email=os.environ.get(
        'EMAIL_CRED')+'@yandex.ru', to=cleaned_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
