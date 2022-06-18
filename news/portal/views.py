from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm, CommentStatusForm
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# для проверки
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError



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
    success_url = '/portal/posts/'



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


class CommentUdateView(UpdateView):
    permission_required = ('news.change_post')
    template_name = 'post.html'
    form_class = CommentStatusForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# def update_comment_status(request, pk, type):
#     return HttpResponse('1')




# для проверки
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Пробное сообщение"
            body = {
                'name': form.cleaned_data['name'],
                'telephone': form.cleaned_data['telephone'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values()) #при переписывании на цифры в формах вылетает ошибка типов
            try:
                send_mail(subject, message,
                          'vachrameev.oleg@yandex.ru',
                          ['vachrameev.oleg@yandex.ru'])
            except BadHeaderError:
                return HttpResponse('Найден некорректный заголовок')
            return redirect("/portal/add")

    form = ContactForm()
    return render(request, "contact.html", {'form': form})
