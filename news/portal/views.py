from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()


class PostAddView(CreateView):
    model = Post
    template_name = 'test.html'
    form_class = PostForm
    success_url = '/'


class PostDetail(DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    form_class = CommentForm
    success_url = '<int:pk>'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.comment_post = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


