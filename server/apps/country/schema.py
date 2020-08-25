from graphene_django_extras import DjangoObjectType, PageGraphqlPagination, \
    DjangoListObjectType, DjangoListObjectField, DjangoObjectField

from apps.contact.schema import ContactListType
from apps.country.models import Country
from apps.organization.schema import OrganizationListType
from utils.fields import DjangoPaginatedListObjectField, CustomDjangoListObjectType


class CountryType(DjangoObjectType):
    class Meta:
        model = Country

    organizations = DjangoPaginatedListObjectField(OrganizationListType,
                                                   pagination=PageGraphqlPagination(
                                                       page_size_query_param='pageSize'
                                                   ))
    contacts = DjangoPaginatedListObjectField(ContactListType,
                                              pagination=PageGraphqlPagination(
                                                  page_size_query_param='pageSize'
                                              ))
    operatingContacts = DjangoPaginatedListObjectField(ContactListType,
                                                       pagination=PageGraphqlPagination(
                                                           page_size_query_param='pageSize'
                                                       ))


class CountryListType(CustomDjangoListObjectType):
    class Meta:
        model = Country
        filter_fields = {
            'name': ['icontains']
        }


class Query:
    country = DjangoObjectField(CountryType)
    country_list = DjangoPaginatedListObjectField(CountryListType,
                                                  pagination=PageGraphqlPagination(
                                                      page_size_query_param='pageSize'
                                                  ))