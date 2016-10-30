from django.core.urlresolvers import reverse

from .base import BaseTestCase
from filebrowser.conf import fb_settings
from filebrowser.functions import get_version_path

import os


class ViewsTest(BaseTestCase):
    """
    Test views
    """
    def test_browse(self):
        response = self.client.get(reverse('fb_browse'))
        self.assertEqual(response.status_code, 200)

        value = os.path.join(self.working_dir, self.image_name)
        version_filename = get_version_path(value, fb_settings.ADMIN_THUMBNAIL)
        os.remove(version_filename)

    def test_mkdir(self):
        response = self.client.get(reverse('fb_mkdir'))
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        response = self.client.get(reverse('fb_upload'))
        self.assertEqual(response.status_code, 200)

    def test_rename(self):
        response = self.client.get(reverse('fb_rename'))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        os.makedirs(os.path.join(self.working_dir, 'test_dir'))

        response = self.client.get(
            '{0}?filename=test_dir&filetype=Folder'.format(
                reverse('fb_delete')
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_versions(self):
        response = self.client.get(reverse('fb_versions'))
        self.assertEqual(response.status_code, 200)
