import django_filters

from apps.entry.models import Entry
from utils.filters import StringListFilter


class EntryFilter(django_filters.FilterSet):
    article_title_contains = django_filters.CharFilter(field_name='article_title', lookup_expr='icontains')
    country = django_filters.NumberFilter(field_name='event__countries', lookup_expr='in')
    countries = StringListFilter(method='filter_countries')

    class Meta:
        model = Entry
        fields = ['event', 'created_by', 'reviewers']

    def filter_countries(self, qs, name, value):
        if not value:
            return qs
        return qs.filter(event__countries__in=value).distinct()

