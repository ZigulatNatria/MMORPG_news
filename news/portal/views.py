from django.shortcuts import render, redirect
from .models import Post, Comments
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required




class PostListView(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.all()


class PostAddView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'test.html'
    form_class = PostForm
    # success_url = 'posts/'

    def post(self, request):
        category = request.POST['category']
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        post = Post.objects.create(category=category, title=title, content=content, author=author)
        post.save()

        return redirect('posts/')


class PostUdateView(LoginRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'test.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/portal/user'



def post(request):
    context = {
        'posts': Post.objects.filter(author=request.user)
    }
    return render(request, 'protect/index.html', context)

class PostDetail(DetailView, FormMixin):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    form_class = CommentForm
    success_url = '<int:pk>'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.get_object().id})

    @method_decorator(login_required)     # Разрешает добавлять комментарии только зарегистрированным пользователям
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


class ProtectPostDetail(DetailView, FormMixin):
    model = Post
    template_name = 'protect/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    form_class = CommentForm
    success_url = '<int:pk>'

    def get_success_url(self):
        return reverse_lazy('post', kwargs={'pk': self.get_object().id})

    @method_decorator(login_required)     # Разрешает добавлять комментарии только зарегистрированным пользователям
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

class CommentDetail(DetailView):
    model = Comments

    template_name = 'change_status.html'

    context_object_name = 'comment'




    def post(self, request, *args, **kwargs):
        # Получаем из POST-запроса статус и первичный ключ комментария
        status = request.POST['status']
        cpk = request.POST['comment_pk']

        # Получаем из базы этот объект и изменяем поле в соответствии с указанным статусом
        comment = Comments.objects.get(pk = cpk)
        if status == 'True':
            comment.status = True
        else:
            comment.status = False

        comment.save()

        return super().get(request, *args, **kwargs)

