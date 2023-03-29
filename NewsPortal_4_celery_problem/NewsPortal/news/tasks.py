from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Post, Category


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
            send_mail(
                subject=f'Новая новость на Вашем любимом новостном портале!',
                message=f'Новая новость "{post.header}" в Вашей любимой категории "{category}"!\n'
                        f'Краткое содержание: {post.short_text}\n',
                        # f'Ссылка на статью: {request.build_absolute_uri(post_url)}',
                from_email='nain9r@mail.ru',
                recipient_list=[user.email],

            )
            print('Email sent to subscriber: ', user.email)