from dataclasses import field
from django_filters import FilterSet, DateFilter, ChoiceFilter, BaseInFilter, CharFilter
from .models import Post
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class CharFilterIn(BaseInFilter, CharFilter):
    pass


class ProductFilter(FilterSet):
    date_field = DateFilter(widget=DateInput, field_name='time_in',
                            lookup_expr='gte', label='Date created is greater or equal to:')
    title = CharFilter(field_name='header', lookup_expr='icontains')
    tag = CharFilterIn(field_name='category__name',
                       lookup_expr='in', label='Category:')

    class Meta:
        model = Post
        fields = ['title', 'tag', 'date_field']
