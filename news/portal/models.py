from django.db import models
from tinymce.models import HTMLField

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
    category = models.CharField(max_length=255, choices=CATEGORY, blank=True)
    title = models.CharField(max_length=50)
    content = HTMLField()

