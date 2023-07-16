from django_filters import FilterSet, DateFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):
    pub_date = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}), lookup_expr='gt')

    class Meta:
        model = Post
        fields = ['header', 'text']
        fields = {
            'header': ['icontains'],
            'text': ['icontains'],

        }