from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.views.generic import CreateView, ListView
from django.http import HttpResponse, HttpResponseRedirect

class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()


class PostAddView(CreateView):
    model = Post
    template_name = 'test.html'
    form_class = PostForm



