from collections import OrderedDict

from django.utils.translation import gettext
from django.conf import settings
from rest_framework import serializers

from apps.contrib.serializers import (
    MetaInformationSerializerMixin,
    UpdateSerializerMixin,
    IntegerIDField,
)
from apps.report.models import (
    Report,
    ReportComment,
    ReportGeneration,
    ReportApproval,
)
from utils.validations import is_child_parent_dates_valid


class ReportSerializer(MetaInformationSerializerMixin,
                       serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'name', 'generated_from', 'analysis', 'methodology',
            'significant_updates', 'challenges', 'summary',
            'filter_figure_regions', 'filter_figure_countries',
            'filter_event_crises', 'filter_figure_categories',
            'filter_figure_start_after', 'filter_figure_end_before',
            'filter_event_crisis_types', 'filter_figure_geographical_groups',
        ]

    def validate(self, attrs) -> dict:
        attrs = super().validate(attrs)
        errors = OrderedDict()
        errors.update(is_child_parent_dates_valid(
            attrs,
            self.instance,
            parent_field=None,
            c_start_field='filter_figure_start_after',
            c_end_field='filter_figure_end_before',
        ))
        if errors:
            raise serializers.ValidationError(errors)
        return attrs


class ReportUpdateSerializer(UpdateSerializerMixin, ReportSerializer):
    id = IntegerIDField(required=True)

    class Meta:
        model = Report
        fields = [
            'id', 'name', 'generated_from', 'analysis', 'methodology',
            'significant_updates', 'challenges', 'summary',
            'filter_figure_regions', 'filter_figure_countries',
            'filter_event_crises', 'filter_figure_categories',
            'filter_figure_start_after', 'filter_figure_end_before',
            'filter_event_crisis_types', 'filter_figure_geographical_groups',
        ]


class ReportCommentSerializer(MetaInformationSerializerMixin,
                              serializers.ModelSerializer):
    class Meta:
        model = ReportComment
        fields = '__all__'

    def validate_body(self, body):
        if not body.strip():
            raise serializers.ValidationError('Comment body is missing.')
        return body


class ReportSignoffSerializer(serializers.Serializer):
    report = serializers.IntegerField(required=True)
    include_history = serializers.BooleanField(required=False)

    def validate_report(self, report):
        if not ReportGeneration.objects.filter(
            report=report,
            is_signed_off=False
        ).exists():
            raise serializers.ValidationError(gettext('Nothing to sign off.'))
        return report

    def save(self):
        report_id = self.validated_data['report']
        report = Report.objects.get(id=report_id)
        report.sign_off(
            self.context['request'].user,
            include_history=self.validated_data.get('include_history', False)
        )
        return report


def is_first_day(date):
    if not date:
        return False
    return date.month == 1 and date.day == 1


def is_last_day(date):
    if not date:
        return False
    return date.month == 12 and date.day == 31


def is_year_equal(foo, bar):
    if not foo:
        return False
    if not bar:
        return False
    return foo.year == bar.year


class ReportGenerationSerializer(MetaInformationSerializerMixin,
                                 serializers.ModelSerializer):
    class Meta:
        model = ReportGeneration
        fields = ['report']

    def validate_report(self, report):
        if (
            report.generated_from == Report.REPORT_TYPE.MASTERFACT or
            not is_first_day(report.filter_figure_start_after) or
            not is_last_day(report.filter_figure_end_before) or
            not is_year_equal(report.filter_figure_start_after, report.filter_figure_end_before)
        ):
            raise serializers.ValidationError(gettext('Cannot start generation for non-grid reports'))
        if ReportGeneration.objects.filter(
            report=report
        ).count() == settings.GRAPHENE_DJANGO_EXTRAS['MAX_PAGE_SIZE']:
            raise serializers.ValidationError(
                # FIXME: this is problematic
                gettext(
                    'Report Generation is limited to %(size)s only.'
                    % {'size': settings.GRAPHENE_DJANGO_EXTRAS['MAX_PAGE_SIZE']}
                )
            )
        if ReportGeneration.objects.filter(
            report=report,
            is_signed_off=False
        ).exists():
            raise serializers.ValidationError(gettext('Cannot start another while previous is not signed off.'))
        return report


class ReportApproveSerializer(serializers.Serializer):
    report = serializers.IntegerField(required=True)
    is_approved = serializers.BooleanField(required=False)

    def validate_report(self, report):
        if not ReportGeneration.objects.filter(
            report_id=report,
            is_signed_off=False
        ).exists():
            raise serializers.ValidationError(gettext('Nothing to approve.'))

        # only one unsigned report can exist, this limit is ensured in ReportGenerationSerializer
        # during generation start...
        if ReportGeneration.objects.get(
            report=report,
            is_signed_off=False,
        ).approvers.count() == settings.GRAPHENE_DJANGO_EXTRAS['MAX_PAGE_SIZE']:
            raise serializers.ValidationError(
                # FIXME: this is problematic
                gettext(
                    'Report Approvals is limited to %(size)s only.'
                    % {'size': settings.GRAPHENE_DJANGO_EXTRAS['MAX_PAGE_SIZE']}
                )
            )
        return report

    def save(self):
        report = self.validated_data['report']
        generation = ReportGeneration.objects.get(
            report_id=report,
            is_signed_off=False,
        )
        ReportApproval.objects.update_or_create(
            generation=generation,
            created_by=self.context['request'].user,
            defaults=dict(
                is_approved=self.validated_data.get('is_approved', True),
            ),
        )
