from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsAdd, ArticleAdd, NewsUpdate, PostDelete

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='search'),
    path('news_add/', NewsAdd.as_view(), name='news_add'),
    path('article_add/', ArticleAdd.as_view(), name='article_add'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
 ]