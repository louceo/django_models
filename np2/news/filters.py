from dataclasses import field
from django_filters import FilterSet, DateFilter, ChoiceFilter, BaseInFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category
from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'


class CharFilterIn(BaseInFilter, CharFilter):
    pass


class ProductFilter(FilterSet):
    date_field = DateFilter(widget=DateInput, field_name='time_in',
                            lookup_expr='gte', label='Date created is greater or equal to:')
    title = CharFilter(field_name='header', lookup_expr='icontains')
    category = ModelChoiceFilter(
        queryset=Category.objects.all(), label='Select categories')

    class Meta:
        model = Post
        fields = ['title', 'category', 'date_field']


class CategoryFilter(FilterSet):
    category = ModelChoiceFilter(
        queryset=Category.objects.all(), label='Search by category')

    class Meta:
        model = Post
        fields = ['category']
