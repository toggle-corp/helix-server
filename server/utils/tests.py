from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import DEFAULT_DB_ALIAS
from django.test import TestCase, override_settings
from graphene_django.utils import GraphQLTestCase

User = get_user_model()


class HelixGraphQLTestCase(GraphQLTestCase):
    GRAPHQL_URL = '/graphql'
    GRAPHQL_SCHEMA = 'helix.schema.schema'

    def create_user(self) -> User:
        raw_password = 'admin123'
        user = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            password=raw_password,
        )
        user.raw_password = raw_password
        return user


class ImmediateOnCommitMixin(object):
    """
    Note: shamelessly copied from https://code.djangoproject.com/ticket/30457

    Will be redundant in immediate_on_commit function is actually implemented in Django 3.2
    Check this PR: https://github.com/django/django/pull/12944
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        def immediate_on_commit(func, using=None):
            func()
        # Context manager executing transaction.on_commit() hooks immediately
        # This is required when using a subclass of django.test.TestCase as all tests are wrapped in
        # a transaction that never gets committed.
        cls.on_commit_mgr = patch('django.db.transaction.on_commit', side_effect=immediate_on_commit)
        cls.on_commit_mgr.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.on_commit_mgr.__exit__()


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'
)
class HelixTestCase(ImmediateOnCommitMixin, TestCase):
    pass