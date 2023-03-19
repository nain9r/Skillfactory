from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
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
    pk_url_kwarg = 'pk'

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
        form = PostForm(request.POST)
        post = form.save(commit=False)
        if len(post.text) > 100:
            post.short_text = post.text[:100] + '...'
        else:
            post.short_text = post.text
        post = form.save()
        post_categories = post.categories.all()
        for category in post_categories:
            for user in Category.objects.get(category=category.category).subscribers.all():
                post_url = reverse('news_detail', args=[post.id])  # генерация URL-адреса статьи
                send_mail(
                    subject=f'Новая статья на Вашем любимом новостном портале!',
                    message=f'Новая статья "{post.header}" в Вашей любимой категории "{category}"!\n'
                            f'Краткое содержание: {post.short_text}\n'
                            f'Ссылка на статью: {request.build_absolute_uri(post_url)}',
                    from_email='nain9r@mail.ru',
                    recipient_list=[user.email],

                )
                print('Email sent to subscriber: ', user.email)
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
    if category.subscribers.filter(pk=user.pk).exists():
        # пользователь уже подписан
        message = f'Вы уже подписаны на категорию "{category.category}"!'
    else:
        # пользователь еще не подписан
        category.subscribers.add(user)
        message = f'Вы успешно подписались на категорию "{category.category}"!'

    return render(
        request,
        'subscribe.html',
        {'category': Category, 'message': message},
    )
