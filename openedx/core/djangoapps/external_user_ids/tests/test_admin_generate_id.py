# """
# Test the logic behind the Generate External IDs tools in Admin
# """
import mock
from django.conf import settings
from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from student.tests.factories import UserFactory

from openedx.core.djangolib.testing.utils import skip_unless_lms

# external_ids is not in CMS' INSTALLED_APPS so these imports will error during test collection
if settings.ROOT_URLCONF == 'lms.urls':
    from openedx.core.djangoapps.external_user_ids.models import (
        ExternalId,
    )
    from openedx.core.djangoapps.external_user_ids.tests.factories import ExternalIDTypeFactory
    from openedx.core.djangoapps.external_user_ids.admin import ExternalIdAdmin


@skip_unless_lms
class TestGenerateExternalIds(TestCase):
    """
    Test generating ExternalIDs for Users.
    """
    def setUp(self):
        super(TestGenerateExternalIds, self).setUp()
        self.users = UserFactory.create_batch(10)
        self.user_id_list = [user.id for user in self.users]
        self.external_id_admin = ExternalIdAdmin(ExternalId, AdminSite())

    def test_generate_ids_for_all_users(self):
        id_type = ExternalIDTypeFactory.create()
        request = mock.Mock()

        assert ExternalId.objects.count() == 0
        self.external_id_admin.process_generate_ids_request(
            user_id_list=self.user_id_list,
            id_type=id_type,
            request=request,
            redirect_url=''
        )
        assert ExternalId.objects.count() == 10

    def test_no_new_for_existing_users(self):
        id_type = ExternalIDTypeFactory.create()
        request = mock.Mock()

        for user in self.users:
            ExternalId.objects.create(
                user=user,
                external_id_type=id_type
            )

        assert ExternalId.objects.count() == 10
        self.external_id_admin.process_generate_ids_request(
            user_id_list=self.user_id_list,
            id_type=id_type,
            request=request,
            redirect_url=''
        )
        assert ExternalId.objects.count() == 10
