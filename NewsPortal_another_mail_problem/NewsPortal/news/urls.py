from django.urls import path
from .views import NewsList, NewsDetail, NewsSearch, NewsAdd, ArticleAdd, PostUpdate, PostDelete, subscribe, CategoryListView, PostCategory
from allauth.account.views import ConfirmEmailView
urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsSearch.as_view(), name='search'),
    path('news_add/', NewsAdd.as_view(), name='news_add'),
    path('article_add/', ArticleAdd.as_view(), name='article_add'),
    path('<int:pk>/edit/',PostUpdate.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path("categories/<int:pk>/subscribe", subscribe, name='subscribe'),
    path('categories/<int:pk>/', PostCategory.as_view(), name='cats'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view(), name='account_confirm_email'),


 ]