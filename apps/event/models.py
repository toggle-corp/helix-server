from collections import OrderedDict

from django.db import models
from django.contrib.postgres.aggregates.general import ArrayAgg
from django.utils.translation import gettext_lazy as _, gettext
from django_enumfield import enum

from apps.contrib.models import (
    MetaInformationAbstractModel,
    MetaInformationArchiveAbstractModel,
)
from apps.crisis.models import Crisis
from apps.contrib.commons import DATE_ACCURACY
from apps.entry.models import Figure, FigureCategory
from apps.users.models import User
from utils.validations import is_child_parent_dates_valid


class NameAttributedModels(models.Model):
    name = models.CharField(_('Name'), max_length=256)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


# Models related to displacement caused by conflict


class Trigger(NameAttributedModels):
    """
    Holds the possible trigger choices
    """


class TriggerSubType(NameAttributedModels):
    """
    Holds the possible trigger sub types
    """


class Violence(NameAttributedModels):
    """
    Holds the possible violence choices
    """


class ViolenceSubType(NameAttributedModels):
    """
    Holds the possible violence sub types
    """
    violence = models.ForeignKey('Violence',
                                 related_name='sub_types', on_delete=models.CASCADE)


class Actor(MetaInformationAbstractModel, NameAttributedModels):
    """
    Conflict related actors
    """
    country = models.ForeignKey('country.Country', verbose_name=_('Country'),
                                null=True,
                                on_delete=models.SET_NULL, related_name='actors')
    # NOTE: torg is used to map actors in the system to it's external source
    torg = models.CharField(verbose_name=_('Torg'), max_length=10, null=True)


# Models related to displacement caused by disaster


class DisasterCategory(NameAttributedModels):
    """
    Holds the possible disaster category choices
    """


class DisasterSubCategory(NameAttributedModels):
    """
    Holds the possible disaster sub categories
    """
    category = models.ForeignKey('DisasterCategory', verbose_name=_('Disaster Category'),
                                 related_name='sub_categories', on_delete=models.CASCADE)


class DisasterType(NameAttributedModels):
    """
    Holds the possible disaster types
    """
    disaster_sub_category = models.ForeignKey('DisasterSubCategory',
                                              verbose_name=_('Disaster Sub Category'),
                                              related_name='types', on_delete=models.CASCADE)


class DisasterSubType(NameAttributedModels):
    """
    Holds the possible disaster sub types
    """
    type = models.ForeignKey('DisasterType', verbose_name=_('Disaster Type'),
                             related_name='sub_types', on_delete=models.CASCADE)


class Event(MetaInformationArchiveAbstractModel, models.Model):
    class EVENT_OTHER_SUB_TYPE(enum.Enum):
        DEVELOPMENT = 0
        EVICTION = 1
        TECHNICAL_DISASTER = 2
        # TODO: add more based on IDMC inputs

        __labels__ = {
            DEVELOPMENT: _('Development'),
            EVICTION: _('Eviction'),
            TECHNICAL_DISASTER: _('Technical disaster'),
        }

    crisis = models.ForeignKey('crisis.Crisis', verbose_name=_('Crisis'),
                               blank=True, null=True,
                               related_name='events', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Event Name'), max_length=256)
    event_type = enum.EnumField(Crisis.CRISIS_TYPE, verbose_name=_('Event Type'))
    other_sub_type = enum.EnumField(EVENT_OTHER_SUB_TYPE, verbose_name=_('Other subtypes'),
                                    blank=True, null=True)
    glide_number = models.CharField(verbose_name=_('Glide Number'), max_length=256,
                                    null=True, blank=True)
    # conflict related fields
    trigger = models.ForeignKey('Trigger', verbose_name=_('Trigger'),
                                blank=True, null=True,
                                related_name='events', on_delete=models.SET_NULL)
    trigger_sub_type = models.ForeignKey('TriggerSubType', verbose_name=_('Trigger Sub-Type'),
                                         blank=True, null=True,
                                         related_name='events', on_delete=models.SET_NULL)
    violence = models.ForeignKey('Violence', verbose_name=_('Violence'),
                                 blank=True, null=True,
                                 related_name='events', on_delete=models.SET_NULL)
    violence_sub_type = models.ForeignKey('ViolenceSubType', verbose_name=_('Violence Sub-Type'),
                                          blank=True, null=True,
                                          related_name='events', on_delete=models.SET_NULL)
    actor = models.ForeignKey('Actor', verbose_name=_('Actors'),
                              blank=True, null=True,
                              related_name='events', on_delete=models.SET_NULL)
    # disaster related fields
    disaster_category = models.ForeignKey('DisasterCategory', verbose_name=_('Disaster Category'),
                                          blank=True, null=True,
                                          related_name='events', on_delete=models.SET_NULL)
    disaster_sub_category = models.ForeignKey('DisasterSubCategory', verbose_name=_('Disaster Sub-Type'),
                                              blank=True, null=True,
                                              related_name='events', on_delete=models.SET_NULL)
    disaster_type = models.ForeignKey('DisasterType', verbose_name=_('Disaster Type'),
                                      blank=True, null=True,
                                      related_name='events', on_delete=models.SET_NULL)
    disaster_sub_type = models.ForeignKey('DisasterSubType', verbose_name=_('Disaster Sub-Type'),
                                          blank=True, null=True,
                                          related_name='events', on_delete=models.SET_NULL)

    countries = models.ManyToManyField('country.Country', verbose_name=_('Countries'),
                                       related_name='events', blank=True)
    start_date = models.DateField(verbose_name=_('Start Date'),
                                  blank=True, null=True)
    start_date_accuracy = enum.EnumField(
        DATE_ACCURACY,
        verbose_name=_('Start Date Accuracy'),
        default=DATE_ACCURACY.DAY,
        blank=True,
        null=True,
    )
    end_date = models.DateField(verbose_name=_('End Date'),
                                blank=True, null=True)
    end_date_accuracy = enum.EnumField(
        DATE_ACCURACY,
        verbose_name=_('End date accuracy'),
        default=DATE_ACCURACY.DAY,
        blank=True,
        null=True,
    )
    event_narrative = models.TextField(verbose_name=_('Event Narrative'),
                                       null=True, blank=True)

    @property
    def total_stock_idp_figures(self) -> int:
        filters = dict(event=self.id)
        return Figure.get_total_stock_idp_figure(filters)

    @property
    def total_flow_nd_figures(self) -> int:
        filters = dict(event=self.id)
        return Figure.get_total_flow_nd_figure(filters)

    @staticmethod
    def clean_dates(values: dict, instance=None) -> OrderedDict:
        # NOTE: There is nothing wrong with moving this to serializers
        return is_child_parent_dates_valid(values, instance, 'crisis')

    @staticmethod
    def clean_by_event_type(values: dict, instance=None) -> OrderedDict:
        errors = OrderedDict()
        event_type = values.get('event_type', getattr(instance, 'event_type', None))
        if event_type == Crisis.CRISIS_TYPE.CONFLICT:
            if not values.get('violence_sub_type', getattr(instance, 'violence_sub_type', None)):
                errors['violence_sub_type'] = gettext('Please mention at least'
                                                      ' the reason for violence.')
        elif event_type == Crisis.CRISIS_TYPE.DISASTER:
            if not values.get('disaster_sub_type', getattr(instance, 'disaster_sub_type', None)):
                errors['disaster_sub_type'] = gettext('Please mention the sub-type of disaster.')
        return errors

    @classmethod
    def get_excel_sheets_data(cls, user_id, filters):
        from apps.event.filters import EventFilter

        class DummyRequest:
            def __init__(self, user):
                self.user = user

        headers = OrderedDict(
            id='Id',
            name='Name',
            crisis='Crisis Id',
            crisis__name='Crisis',
            start_date='Start Date',
            start_date_accuracy='Start Date Accuracy',
            end_date='End Date',
            end_date_accuracy='End Date Accuracy',
            countries_iso3='ISO3',
            countries_name='Geo Names',
            regions_name='Geo Regions',
            figures_count='Figures Count',
            figures_sum='Reocmmended figures',
            created_at='Created At',
            created_by__full_name='Created By',
            event_type='Event Type',
            other_sub_type='Other Sub Type',
            trigger__name='Trigger',
            trigger_sub_type__name='Trigger Subtype',
            violence__name='Violence',
            violence_sub_type__name='Violence Subtype',
            actor_id='Actor Id',
            actor__name='Actor',
            disaster_category__name='Disaster Category',
            disaster_sub_category__name='Disaster Subcategory',
            disaster_type__name='Disaster Type',
            disaster_sub_type__name='Disaster Sub Type',
        )
        values = EventFilter(
            data=filters,
            request=DummyRequest(user=User.objects.get(id=user_id)),
        ).qs.annotate(
            countries_iso3=ArrayAgg('countries__iso3', distinct=True),
            countries_name=ArrayAgg('countries__name', distinct=True),
            regions_name=ArrayAgg('countries__region__name', distinct=True),
            figures_sum=models.Sum(
                'entries__figures__total_figures',
                filter=models.Q(
                    entries__figures__category=FigureCategory.flow_new_displacement_id(),
                    entries__figures__role=Figure.ROLE.RECOMMENDED,
                ),
            ),
            figures_count=models.Count('entries__figures', distinct=True),
        ).order_by('-created_at').select_related(
            'trigger',
            'trigger_sub_type',
            'violence',
            'violence_sub_type',
            'actor',
            'disaster_category',
            'disaster_sub_category',
            'disaster_type',
            'disaster_sub_type',
            'created_at',
        ).prefetch_related(
            'countries',
        ).values(*[header for header in headers.keys()])
        data = [
            {
                **datum,
                **dict(
                    start_date_accuracy=getattr(DATE_ACCURACY.get(datum['start_date_accuracy']), 'name', ''),
                    end_date_accuracy=getattr(DATE_ACCURACY.get(datum['end_date_accuracy']), 'name', ''),
                    event_type=getattr(Crisis.CRISIS_TYPE.get(datum['event_type']), 'name', ''),
                    other_sub_type=getattr(Event.EVENT_OTHER_SUB_TYPE.get(datum['other_sub_type']), 'name', ''),
                )
            }
            for datum in values
        ]

        return {
            'headers': headers,
            'data': data,
            'formulae': None,
        }

    def save(self, *args, **kwargs):
        if self.disaster_sub_type:
            self.disaster_type = self.disaster_sub_type.type
            self.disaster_sub_category = self.disaster_type.disaster_sub_category
            self.disaster_category = self.disaster_sub_category.category
        if self.violence_sub_type:
            self.violence = self.violence_sub_type.violence
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name or str(self.id)
