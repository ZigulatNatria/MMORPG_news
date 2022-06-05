from django.forms import ModelForm
from .models import Post
from tinymce.widgets import TinyMCE
from django.forms import CharField

class PostForm(ModelForm):

    content = CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30})) # Виджет редактора

    class Meta:
        model = Post
        fields = '__all__'