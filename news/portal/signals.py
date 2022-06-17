from django.dispatch import receiver
from .models import Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.contrib.auth.models import User


@receiver(post_save, sender= Post)
def new_post_created(sender, instance, created, **kwargs):
    if created:
        title = Post.objects.get(id= instance.id).title
        content = Post.objects.get(id= instance.id).content
        qs = User.objects.filter(User.email).values('email')

        msg = EmailMultiAlternatives(
            subject=title,
            body=f'{content}',  # это то же, что и message
            from_email='vachrameev.oleg@yandex.ru',
            to=[qs],  # это то же, что и recipients_list
        )
        msg.send()  # отсылаем