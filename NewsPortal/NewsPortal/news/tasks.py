from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Post, Category
from django.db.models import Prefetch
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
import logging
logger = logging.getLogger(__name__)


@shared_task
def send_notifications(post_pk):
    post = Post.objects.get(id=post_pk)
    post_categories = post.categories.all()
    if len(post.text) > 100:
        post.short_text = post.text[:100] + '...'
    else:
        post.short_text = post.text
    for category in post_categories:
        for user in Category.objects.get(category=category.category).subscribers.all():
            try:
                send_mail(
                    subject=f'Новая новость на Вашем любимом новостном портале!',
                    message=f'Новая новость "{post.header}" в Вашей любимой категории "{category}"!\n'
                        f'Краткое содержание: {post.short_text}\n',
                    from_email='nain9r@mail.ru',
                )
            except Exception as e:
                logger.exception('Error sending email: %s', e)

            print('Email sent to subscriber: ', user.email)


@shared_task
def weekly_news():
    categories = Category.objects.prefetch_related(
            Prefetch('subscribers', queryset=User.objects.all()))
    articles_by_category = {}
    last_week = timezone.now() - timedelta(days=7)
    for category in categories:
        articles = Post.objects.filter(categories=category, pub_date__gte=last_week)
        articles_by_category[category.category] = articles
    for category in categories:
        for subscriber in category.subscribers.all():
            email = subscriber.email
            subject = "Еженедельная новостная рассылка от Вашего любимого новостного портала!"
            articles = articles_by_category[category.category]
            if articles:
                message = f'Новые статьи в категории "{category.category}" за прошедшую неделю:\n\n'
                for article in articles:
                    message += f'Статья {article.header}: \n{settings.BASE_URL}/news/{article.id}\n\n'
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])