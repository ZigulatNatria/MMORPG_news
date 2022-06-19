from django.forms import ModelForm, CharField, Textarea
from .models import Post, Comments
from tinymce.widgets import TinyMCE
from django import forms

class PostForm(ModelForm):

    content = CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30})) # Виджет редактора

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'content',
        ]



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows':5})

