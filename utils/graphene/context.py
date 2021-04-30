from django.utils.functional import cached_property

from apps.country.dataloaders import TotalFigureThisYearByCountryCategoryLoader


class GQLContext:
    def __init__(self, request):
        self.request = request

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def country_country_this_year_idps_loader(self):
        from apps.entry.models import FigureCategory
        return TotalFigureThisYearByCountryCategoryLoader(
            category=FigureCategory.stock_idp_id()
        )

    @cached_property
    def country_country_this_year_nd_loader(self):
        from apps.entry.models import FigureCategory
        return TotalFigureThisYearByCountryCategoryLoader(
            category=FigureCategory.flow_new_displacement_id()
        )
