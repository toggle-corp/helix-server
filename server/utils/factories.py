import factory
from dateutil.utils import today
from factory.django import DjangoModelFactory

from apps.contact.models import Contact
from apps.crisis.models import Crisis


class UserFactory(DjangoModelFactory):
    class Meta:
        model = 'users.User'

    email = factory.Sequence(lambda n: f'admin{n}@email.com')
    username = factory.Sequence(lambda n: f'username{n}')


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = 'country.Country'


class OrganizationKindFactory(DjangoModelFactory):
    class Meta:
        model = 'organization.OrganizationKind'

    title = factory.Faker('company_suffix')


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = 'organization.Organization'


class ContactFactory(DjangoModelFactory):
    class Meta:
        model = 'contact.Contact'

    designation = factory.Iterator(Contact.DESIGNATION)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    gender = factory.Iterator(Contact.GENDER)
    job_title = factory.Faker('job')
    organization = factory.SubFactory(OrganizationFactory)


class DisasterCategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'event.DisasterCategory'


class ViolenceFactory(DjangoModelFactory):
    class Meta:
        model = 'event.Violence'


class CrisisFactory(DjangoModelFactory):
    class Meta:
        model = 'crisis.Crisis'

    crisis_type = factory.Iterator(Crisis.CRISIS_TYPE)


class EventFactory(DjangoModelFactory):
    class Meta:
        model = 'event.Event'

    crisis = factory.SubFactory(CrisisFactory)
    event_type = factory.Iterator(Crisis.CRISIS_TYPE)


class EntryFactory(DjangoModelFactory):
    class Meta:
        model = 'entry.Entry'

    article_title = factory.Sequence(lambda n: f'long title {n}')
    source = factory.Faker('company')
    publisher = factory.Faker('company')
    publish_date = factory.LazyFunction(today().date)
    source_breakdown = factory.Sequence(lambda n: f'long text breakdown {n}')
    event = factory.SubFactory(EventFactory)
    tags = factory.Sequence(lambda n: [f'tag{each}' for each in range(n % 10)])
