from celery import shared_task
import time
import os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from . import models
import datetime
from django.contrib.auth import get_user_model
from np2 import settings


@shared_task
def notify_subscribers_async(html_content, sub, msg, cleaned_emails, from_email):
    # time.sleep(10)
    msg = EmailMultiAlternatives(
        subject=sub, body=msg, from_email=from_email, to=cleaned_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def weekly_newsletter_async():
    date = datetime.datetime.now() - datetime.timedelta(days=7)
    weekly_posts = models.Post.objects.filter(time_in__gte=date)
    user_emails = get_user_model().objects.all().values_list(
        'email', flat=True).filter(email__contains='@')

    html_content = render_to_string(
        'weekly_newsletter.html', {'posts': weekly_posts})

    msg = EmailMultiAlternatives(
        subject=f'News for this week!', from_email=settings.EMAIL_HOST_USER, to=user_emails)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
