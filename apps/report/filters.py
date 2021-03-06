from django_filters import rest_framework as df

from apps.report.models import Report
from utils.filters import IDListFilter


class ReportFilter(df.FilterSet):
    filter_figure_countries = IDListFilter(method='filter_countries')

    class Meta:
        model = Report
        fields = {
            'name': ['icontains'],
        }

    def filter_countries(self, qs, name, value):
        if value:
            return qs.filter(filter_figure_countries__in=value).distinct()
        return qs

    @property
    def qs(self):
        return super().qs.distinct()


class CountryReportFilter(df.FilterSet):
    """
    NOTE: following fields are predefined and annotated into the queryset
    """
    country = df.CharFilter(field_name='id', lookup_expr='exact')
