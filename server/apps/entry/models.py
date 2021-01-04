from collections import OrderedDict
import json
import logging
import uuid

import boto3
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _, gettext
from django_enumfield import enum

from apps.contrib.models import (
    MetaInformationAbstractModel,
    UUIDAbstractModel,
    MetaInformationArchiveAbstractModel,
)
from apps.entry.constants import STOCK, FLOW
from apps.users.enums import USER_ROLE
from apps.review.models import Review

from utils.fields import CachedFileField

logger = logging.getLogger(__name__)
User = get_user_model()
CANNOT_UPDATE_MESSAGE = _('You cannot sign off the entry.')


class SourcePreview(MetaInformationAbstractModel):
    PREVIEW_FOLDER = 'source/previews'

    url = models.URLField(verbose_name=_('Source URL'))
    token = models.CharField(verbose_name=_('Token'),
                             max_length=64, db_index=True,
                             blank=True, null=True)
    pdf = CachedFileField(verbose_name=_('Rendered Pdf'),
                          blank=True, null=True,
                          upload_to=PREVIEW_FOLDER)
    completed = models.BooleanField(default=False)
    reason = models.TextField(verbose_name=_('Error Reason'),
                              blank=True, null=True)

    @classmethod
    def get_pdf(cls, url: str, instance: 'SourcePreview' = None, **kwargs) -> 'SourcePreview':
        """
        Based on the url, generate a pdf and store it.
        """
        if not instance:
            token = str(uuid.uuid4())
            instance = cls(token=token)
        instance.url = url
        # TODO: remove .pdf in production... this will happen after webhook
        instance.pdf = cls.PREVIEW_FOLDER + '/' + instance.token + '.pdf'

        instance.save()

        payload = dict(
            url=url,
            token=instance.token,
            filename=f'{instance.token}.pdf',
        )
        logger.info(f'Invoking lambda function for preview {url} {instance.token}')
        client = boto3.client('lambda')
        client.invoke(
            FunctionName=settings.LAMBDA_HTML_TO_PDF,
            InvocationType='Event',
            Payload=json.dumps(payload)
        )
        return instance


class OSMName(UUIDAbstractModel, models.Model):
    class OSM_ACCURACY(enum.Enum):
        ADMIN = 0
        POINT = 1

        __labels__ = {
            ADMIN: _('Admin'),
            POINT: _('Point'),
        }

    class IDENTIFIER(enum.Enum):
        SOURCE = 0
        DESTINATION = 1

        __labels__ = {
            SOURCE: _('Source'),
            DESTINATION: _('Destination'),
        }

    # external API fields
    wikipedia = models.TextField(verbose_name=_('Wikipedia'),
                                 blank=True, null=True)
    rank = models.IntegerField(verbose_name=_('Rank'),
                               blank=True, null=True)
    country = models.TextField(verbose_name=_('Country'))
    country_code = models.CharField(verbose_name=_('Country Code'), max_length=8)
    street = models.TextField(verbose_name=_('Street'),
                              blank=True, null=True)
    wiki_data = models.TextField(verbose_name=_('Wiki data'),
                                 blank=True, null=True)
    osm_id = models.CharField(verbose_name=_('OSM Id'), max_length=256)
    osm_type = models.CharField(verbose_name=_('OSM Type'), max_length=256)
    house_numbers = models.TextField(verbose_name=_('House numbers'),
                                     blank=True, null=True)
    identifier = enum.EnumField(verbose_name=_('Identifier'), enum=IDENTIFIER)
    city = models.CharField(verbose_name=_('City'), max_length=256,
                            blank=True, null=True)
    display_name = models.CharField(verbose_name=_('Display name'), max_length=512)
    lon = models.FloatField(verbose_name=_('Longitude'))
    lat = models.FloatField(verbose_name=_('Latitude'))
    state = models.TextField(verbose_name=_('State'),
                             blank=True, null=True)
    bounding_box = ArrayField(verbose_name=_('Bounding Box'),
                              base_field=models.FloatField(),
                              blank=True, null=True)
    type = models.TextField(verbose_name=_('Type'),
                            blank=True, null=True)
    importance = models.FloatField(verbose_name=_('Importance'),
                                   blank=True, null=True)
    class_name = models.TextField(verbose_name=_('Class'),
                                  blank=True, null=True)
    name = models.TextField(verbose_name=_('Name'))
    name_suffix = models.TextField(verbose_name=_('Name Suffix'),
                                   blank=True, null=True)
    place_rank = models.IntegerField(verbose_name=_('Place Rank'),
                                     blank=True, null=True)
    alternative_names = models.TextField(verbose_name=_('Alternative names'),
                                         blank=True, null=True)
    # custom fields
    accuracy = enum.EnumField(verbose_name=_('Accuracy'),
                              enum=OSM_ACCURACY)
    reported_name = models.TextField(verbose_name=_('Reported Name'))
    moved = models.BooleanField(verbose_name=_('Moved'),
                                default=False)


class FigureCategory(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=8)
    type = models.CharField(verbose_name=_('Type'), max_length=8, choices=(
        (STOCK, STOCK),
        (FLOW, FLOW),
    ), default=STOCK)


class Figure(MetaInformationArchiveAbstractModel, UUIDAbstractModel, models.Model):
    class TYPE(enum.Enum):  # temp filler for migration file
        pass

    class QUANTIFIER(enum.Enum):
        MORE_THAN = 0
        LESS_THAN = 1
        EXACT = 2
        APPROXIMATELY = 3

        __labels__ = {
            MORE_THAN: _("More than"),
            LESS_THAN: _("Less than"),
            EXACT: _("Exact"),
            APPROXIMATELY: _("Approximately"),
        }

    class UNIT(enum.Enum):
        PERSON = 0
        HOUSEHOLD = 1

        __labels__ = {
            PERSON: _("Person"),
            HOUSEHOLD: _("Household"),
        }

    class TERM(enum.Enum):
        EVACUATED = 0
        DISPLACED = 1
        DESTROYED_HOUSING = 2
        PARTIALLY_DESTROYED_HOUSING = 3
        UNINHABITABLE_HOUSING = 4
        FORCED_TO_FLEE = 5
        HOMELESS = 6
        IN_RELIEF_CAMP = 7
        SHELTERED = 8
        RELOCATED = 9
        AFFECTED = 10
        RETURNS = 11
        MULTIPLE_OR_OTHER = 12

        __labels__ = {
            EVACUATED: _("Evacuated"),
            DISPLACED: _("Displaced"),
            DESTROYED_HOUSING: _("Destroyed housing"),
            PARTIALLY_DESTROYED_HOUSING: _("Partially destroyed housing"),
            UNINHABITABLE_HOUSING: _("Uninhabitable housing"),
            FORCED_TO_FLEE: _("Forced to flee"),
            HOMELESS: _("Homeless"),
            IN_RELIEF_CAMP: _("In relief camp"),
            SHELTERED: _("Sheltered"),
            RELOCATED: _("Relocated"),
            AFFECTED: _("Affected"),
            RETURNS: _("Returns"),
            MULTIPLE_OR_OTHER: _("Multiple/Other"),
        }

    class ROLE(enum.Enum):
        RECOMMENDED = 0
        PARTIAL_ADDED = 1
        PARTIAL_SUBTRACTED = 2
        TRIANGULATION = 3

        __labels__ = {
            RECOMMENDED: _("Recommended figure"),
            PARTIAL_ADDED: _("Partial figure (Added)"),
            PARTIAL_SUBTRACTED: _("Partial figure (Subtracted)"),
            TRIANGULATION: _("Triangulation"),
        }

    entry = models.ForeignKey('Entry', verbose_name=_('Entry'),
                              related_name='figures', on_delete=models.CASCADE)
    district = models.TextField(verbose_name=_('District(s)'))
    town = models.CharField(verbose_name=_('Town/Village'), max_length=256)
    quantifier = enum.EnumField(enum=QUANTIFIER, verbose_name=_('Quantifier'))
    reported = models.PositiveIntegerField(verbose_name=_('Reported Figures'))
    unit = enum.EnumField(enum=UNIT, verbose_name=_('Unit of Figure'), default=UNIT.PERSON)
    household_size = models.PositiveSmallIntegerField(verbose_name=_('Household Size'),
                                                      blank=True, null=True)
    total_figures = models.PositiveIntegerField(verbose_name=_('Total Figures'), default=0,
                                                editable=False)
    term = enum.EnumField(enum=TERM, verbose_name=_('Term'), default=TERM.EVACUATED)
    category = models.ForeignKey('FigureCategory', verbose_name=_('Figure category'),
                                 related_name='figures', on_delete=models.PROTECT,
                                 blank=False, null=True)
    role = enum.EnumField(enum=ROLE, verbose_name=_('Role'), default=ROLE.RECOMMENDED)

    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'),
                                blank=True, null=True)
    include_idu = models.BooleanField(verbose_name=_('Include in IDU'))
    excerpt_idu = models.TextField(verbose_name=_('Excerpt for IDU'),
                                   blank=True, null=True)

    country = models.ForeignKey('country.Country', verbose_name=_('Country'),
                                blank=True, null=True,
                                related_name='figures', on_delete=models.SET_NULL)

    is_disaggregated = models.BooleanField(verbose_name=_('Is disaggregated'),
                                           default=False)
    # disaggregation information
    displacement_urban = models.PositiveIntegerField(verbose_name=_('Displacement/Urban'),
                                                     blank=True, null=True)
    displacement_rural = models.PositiveIntegerField(verbose_name=_('Displacement/Rural'),
                                                     blank=True, null=True)
    location_camp = models.PositiveIntegerField(verbose_name=_('Location/Camp'),
                                                blank=True, null=True)
    location_non_camp = models.PositiveIntegerField(verbose_name=_('Location/Non-Camp'),
                                                    blank=True, null=True)
    sex_male = models.PositiveIntegerField(verbose_name=_('Sex/Male'),
                                           blank=True, null=True)
    sex_female = models.PositiveIntegerField(verbose_name=_('Sex/Female'),
                                             blank=True, null=True)
    age_json = ArrayField(base_field=JSONField(verbose_name=_('Age')),
                          verbose_name=_('Age Disaggregation'),
                          blank=True, null=True)
    strata_json = ArrayField(base_field=JSONField(verbose_name=_('Stratum')),
                             verbose_name=_('Strata Disaggregation'),
                             blank=True, null=True)
    # conflict based disaggregation
    conflict = models.PositiveIntegerField(verbose_name=_('Conflict/Conflict'),
                                           blank=True, null=True)
    conflict_political = models.PositiveIntegerField(verbose_name=_('Conflict/Violence-Political'),
                                                     blank=True, null=True)
    conflict_criminal = models.PositiveIntegerField(verbose_name=_('Conflict/Violence-Criminal'),
                                                    blank=True, null=True)
    conflict_communal = models.PositiveIntegerField(verbose_name=_('Conflict/Violence-Communal'),
                                                    blank=True, null=True)
    conflict_other = models.PositiveIntegerField(verbose_name=_('Other'),
                                                 blank=True, null=True)
    # locations
    geo_locations = models.ManyToManyField('OSMName', verbose_name=_('Geo Locations'),
                                           related_name='+')

    @classmethod
    def can_be_created_by(cls, user: User, entry: 'Entry') -> bool:
        return entry.can_be_updated_by(user)

    def can_be_updated_by(self, user: User) -> bool:
        """
        used to check before deleting as well
        """
        return self.entry.can_be_updated_by(user)

    @staticmethod
    def clean_idu(values: dict, instance=None) -> OrderedDict:
        errors = OrderedDict()
        if values.get('include_idu', getattr(instance, 'include_idu', None)):
            excerpt_idu = values.get('excerpt_idu', getattr(instance, 'excerpt_idu', None))
            if excerpt_idu is None or not excerpt_idu.strip():
                errors['excerpt_idu'] = gettext('This field is required. ')
        return errors

    def save(self, *args, **kwargs):
        # TODO: set household size from the country
        self.total_figures = self.reported
        if self.unit == self.UNIT.HOUSEHOLD:
            self.total_figures = self.reported * self.household_size
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.quantifier.label} {self.reported} {self.term.label}'


class FigureTag(MetaInformationAbstractModel):
    name = models.CharField(verbose_name=_('Name'), max_length=256)


class Entry(MetaInformationArchiveAbstractModel, models.Model):
    url = models.URLField(verbose_name=_('Source URL'),
                          blank=True, null=True)
    preview = models.OneToOneField('SourcePreview',
                                   related_name='entry', on_delete=models.SET_NULL,
                                   blank=True, null=True,
                                   help_text=_('After the preview has been generated pass its id'
                                               'along during entry creation, so that during entry '
                                               'update the preview can be obtained.'))
    document = models.ForeignKey('contrib.Attachment', verbose_name='Attachment',
                                 on_delete=models.CASCADE, related_name='+',
                                 null=True, blank=True)
    article_title = models.TextField(verbose_name=_('Article Title'))
    sources = models.ManyToManyField('organization.Organization', verbose_name=_('Source'),
                                     blank=True, related_name='sourced_entries')
    publishers = models.ManyToManyField('organization.Organization', verbose_name=_('Publisher'),
                                        blank=True, related_name='published_entries')
    publish_date = models.DateField(verbose_name=_('Published Date'))
    source_excerpt = models.TextField(verbose_name=_('Excerpt from Source'),
                                      blank=True, null=True)
    event = models.ForeignKey('event.Event', verbose_name=_('Event'),
                              related_name='entries', on_delete=models.CASCADE)

    idmc_analysis = models.TextField(verbose_name=_('IDMC Analysis'),
                                     blank=False, null=True)
    calculation_logic = models.TextField(verbose_name=_('Calculation Logic'),
                                         blank=True, null=True)
    is_confidential = models.BooleanField(
        verbose_name=_('Confidential Source'),
        default=False,
    )
    caveats = models.TextField(verbose_name=_('Caveats'), blank=True, null=True)
    # TODO: grid
    tags = models.ManyToManyField('FigureTag', blank=True)

    # TODO: restrict guest users here
    reviewers = models.ManyToManyField('users.User', verbose_name=_('Reviewers'),
                                       blank=True,
                                       related_name='review_entries',
                                       through='EntryReviewer',
                                       through_fields=('entry', 'reviewer'))

    @property
    def latest_reviews(self):
        return self.reviews.order_by(
            *Review.UNIQUE_TOGETHER_WITHOUT_ENTRY_FIELDS, '-created_at'
        ).distinct(
            *Review.UNIQUE_TOGETHER_WITHOUT_ENTRY_FIELDS
        )

    @property
    def source_methodology(self) -> str:
        return getattr(self.source, 'methodology', '')

    @property
    def total_figures(self) -> int:
        return self.figures.aggregate(total=Sum('total_figures'))['total']

    @staticmethod
    def clean_url_and_document(values: dict, instance=None) -> OrderedDict:
        errors = OrderedDict()
        if instance:
            # we wont allow updates to entry sources
            return errors
        url = values.get('url', getattr(instance, 'url', None))
        document = values.get('document', getattr(instance, 'document', None))
        if not url and not document:
            errors['url'] = gettext('Please fill the URL or upload a document. ')
            errors['document'] = gettext('Please fill the URL or upload a document. ')
        return errors

    @property
    def locked(self):
        return self.reviewers.through.objects.filter(
            status=EntryReviewer.REVIEW_STATUS.SIGNED_OFF
        ).exists()

    def can_be_updated_by(self, user: User) -> bool:
        """
        used to check before deleting as well
            i.e `can be DELETED by`
        """
        if self.locked:
            return False
        if USER_ROLE.ADMIN.name in user.groups.values_list('name', flat=True):
            return True
        return self.created_by == user

    def __str__(self):
        return f'Entry {self.article_title}'

    class Meta:
        permissions = (('sign_off_entry', 'Can sign off the entry'),)


class EntryReviewer(MetaInformationAbstractModel, models.Model):
    class CannotUpdateStatusException(Exception):
        message = CANNOT_UPDATE_MESSAGE

    class REVIEW_STATUS(enum.Enum):
        UNDER_REVIEW = 0
        REVIEW_COMPLETED = 1
        SIGNED_OFF = 2
        TO_BE_REVIEWED = 3

        __labels__ = {
            UNDER_REVIEW: _("Under Review"),
            REVIEW_COMPLETED: _("Review Completed"),
            SIGNED_OFF: _("Signed Off"),
            TO_BE_REVIEWED: _("To be reviewed"),
        }

    entry = models.ForeignKey(Entry, verbose_name=_('Entry'),
                              related_name='reviewing', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('users.User', verbose_name=_('Reviewer'),
                                 related_name='reviewing', on_delete=models.CASCADE)
    status = enum.EnumField(enum=REVIEW_STATUS, verbose_name=_('Review Status'),
                            default=REVIEW_STATUS.TO_BE_REVIEWED)

    def __str__(self):
        return f'{self.entry_id} {self.reviewer} {self.status}'

    @classmethod
    def assign_creator(cls, entry: 'Entry', user: 'User') -> None:
        entry.reviewers.through.objects.filter(
            created_by__isnull=True
        ).update(created_by=user)

    def update_status(self, status: REVIEW_STATUS) -> None:
        if status == self.REVIEW_STATUS.SIGNED_OFF \
                and not self.reviewer.has_perms(('entry.sign_off_entry',)):
            raise self.CannotUpdateStatusException()
        self.status = status

    def save(self, *args, **kwargs):
        self.update_status(self.status)
        return super().save(*args, **kwargs)
