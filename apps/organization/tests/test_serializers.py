from django.test import RequestFactory

from apps.contact.models import Contact
from apps.organization.serializers import OrganizationSerializer
from utils.tests import HelixTestCase


class TestCreateOrganizationSerializer(HelixTestCase):
    def setUp(self) -> None:
        self.data = {
            "name": "org name",
            "short_name": "org1",
            "methodology": "source1",
            "contacts": [
                {
                    "designation": Contact.DESIGNATION.MR.value,
                    "first_name": "test",
                    "last_name": "last",
                    "gender": Contact.GENDER.MALE.value,
                    "job_title": "job",
                    "phone": "9989999"
                },
            ]
        }
        self.context = dict(
            request=RequestFactory().post('/graphql')
        )

    def test_valid_serializer(self):
        serializer = OrganizationSerializer(data=self.data, context=self.context)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        organization = serializer.save()
        self.assertEqual(organization.contacts.count(), len(self.data['contacts']))