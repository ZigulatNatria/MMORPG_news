from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from .middleware import get_current_user
from django.db.models import Q #в запросе позволяет создать условие "И"

class Post(models.Model):
    CATEGORY = (
        ('Танки', 'Танки'),
        ('Хилы', 'Хилы'),
        ('ДД', 'ДД'),
        ('Торговцы', 'Торговцы'),
        ('Гилдмастеры', 'Гилдмастеры'),
        ('Квестгиверы', 'Квестгиверы'),
        ('Кузнецы', 'Кузнецы'),
        ('Кожевенники', 'Кожевенники'),
        ('Зельевары', 'Зельевары'),
        ('Мастера заклинаний', 'Мастера Заклинаний')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=CATEGORY, blank=True)
    title = models.CharField(max_length=50)
    content = HTMLField()

class StatusFilterComments(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(Q(status=False, author=get_current_user()) |
                                             Q(status=False, comment_post__author=get_current_user()) | Q(status=True))

class Comments(models.Model):
    comment_post = models.ForeignKey(Post, on_delete = models.CASCADE, verbose_name='Статья', blank = True, null = True, related_name='comments_post')
    author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name='Автор комментария', blank = True, null = True )
    create_date = models.DateTimeField(auto_now=True)
    text = models.TextField()
    status = models.BooleanField(verbose_name='Видимость статьи', default=False)
    objects = StatusFilterComments()