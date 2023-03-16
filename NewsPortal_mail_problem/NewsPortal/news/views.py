from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.shortcuts import render, redirect

class NewsList(ListView):
    model = Post
    ordering = 'pub_date'
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10


class NewsDetail(DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsSearch(ListView):
    model = Post
    ordering = 'pub_date'
    template_name = 'search.html'
    context_object_name = 'news_list'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsAdd(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_add.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "n"
        self.template_name = 'news_add.html'
        self.success_url = reverse_lazy('news_add')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ArticleAdd(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'article_add.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = "a"
        self.template_name = 'article_add.html'
        self.success_url = reverse_lazy('article_add')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        '''Отправляет письмо подписчикам после создания нового поста'''
        form = PostForm(request.POST)
        post = form.save()
        post_categories = post.categories.all()
        list_of_users = []
        for category in post_categories:
            for i in range(len(Category.objects.get(category=category).subscribers.all())):
                list_of_users.append(Category.objects.get(category=category).subscribers.all()[i].email)
        send_mail(
            subject='Новый пост на портале newsportal!',
            message=f'Новая статья { Post.header } в Вашей любимой категории {category}!',
            from_email='haxerwf@yandex.ru',
            recipient_list=list_of_users,
        )
        return redirect('article_add')


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news/'


class CategoryListView(ListView):
    model = Category
    template_name = 'Category_list.html'
    context_object_name = 'categories'


class PostCategory(ListView):
    model = Post
    template_name = 'cats.html'
    context_object_name = 'cats'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(categories=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = Post.objects.filter(categories=self.kwargs['pk'])
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'вы успешно подписались на рассылку по категории'
    return render(
        request,
        'subscribe.html',
        {'category': category, 'message': message},
    )


