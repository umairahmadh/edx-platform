"""
Tests for external id models.
"""
from django.test import TestCase

from student.tests.factories import UserFactory
from ..models import ExternalId


class TestModels(TestCase):
    def test_create_type(self):
        user = UserFactory(is_staff=False)
        ext_id, created = ExternalId.add_new_user_id(user, 'test', create_type=True)
        assert ext_id.external_id_type.description == 'auto generated'
        same_id, created = ExternalId.add_new_user_id(user, 'test', create_type=True)
        assert not created
        assert ext_id == same_id
