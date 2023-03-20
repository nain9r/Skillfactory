from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from django.utils import timezone
from ...models import Post, Category
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from django.db.models import Prefetch
from django.contrib.auth.models import User
from django.conf import settings
import logging.config


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.handle, 'interval', weeks=1, id='send_weekly_articles')
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
                    print('Email sent to subscriber: ', subscriber.email)
            logger.info("Starting scheduler...")
            scheduler.start()


