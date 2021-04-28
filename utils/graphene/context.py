from django.utils.functional import cached_property

from apps.country.dataloaders import TotalFigureByCountryCategoryLoader


class GQLContext:
    def __init__(self, request):
        self.request = request

    @cached_property
    def user(self):
        return self.request.user

    @cached_property
    def country_idp_figure_dataloader(self):
        from apps.entry.models import FigureCategory
        return TotalFigureByCountryCategoryLoader(
            category=FigureCategory.stock_idp_id()
        )

    @cached_property
    def country_nd_figure_dataloader(self):
        from apps.entry.models import FigureCategory
        return TotalFigureByCountryCategoryLoader(
            category=FigureCategory.flow_new_displacement_id()
        )
