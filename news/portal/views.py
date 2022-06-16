from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm, CommentForm
from django.views.generic import CreateView, ListView, DetailView
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
    success_url = 'posts/'


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
