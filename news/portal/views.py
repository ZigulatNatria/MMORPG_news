from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.views.generic.edit import CreateView
from django.http import HttpResponse, HttpResponseRedirect



class PostAddView(CreateView):
    model = Post
    template_name = 'test.html'
    form_class = PostForm



