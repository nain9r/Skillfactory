from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin


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


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ('news.change_post',)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/news/'