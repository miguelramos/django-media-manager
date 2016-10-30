from django.core.urlresolvers import reverse

from .base import BaseTestCase
from filebrowser.conf import fb_settings
from filebrowser.functions import get_version_path

import os


class FbCsrfTokenTests(BaseTestCase):
    """
    Test template tags from fb_pagination
    """
    def test_pagination(self):
        response = self.client.get(reverse('fb_browse'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get('{0}?p=2'.format(reverse('fb_browse')))
        self.assertEqual(response.status_code, 200)


class FbTagsTests(BaseTestCase):
    """
    Test template tags from fb_tags
    """
    def test_query_string(self):
        response = self.client.get('{0}?p=2'.format(reverse('fb_browse')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.wsgi_request.GET), 1)

    def test_selectable(self):
        response = self.client.get('{0}?pop=3'.format(reverse('fb_browse')))
        needle = '<button class="button fb_selectlink" onclick="OpenFile' \
                 '(ProtectPath(\'/media/uploads/test_file.jpg\'));' \
                 'return false;">Select</button>'
        self.assertInHTML(needle, response.content.decode('utf-8'))


class FbVersionsTests(BaseTestCase):
    """
    Test template tags from fb_versions
    """
    def test_version(self):
        value = os.path.join(self.working_dir, self.image_name)
        version_filename = get_version_path(value, fb_settings.ADMIN_THUMBNAIL)
        self.assertTrue(os.path.isfile(version_filename))
        os.remove(version_filename)

    def test_version_object(self):
        url = '{0}?filename={1}'.format(reverse('fb_versions'),
                                        self.image_name)
        self.client.get(url)

        for version in fb_settings.ADMIN_VERSIONS:
            value = os.path.join(self.working_dir, self.image_name)
            version_filename = get_version_path(value, version)
            self.assertTrue(os.path.isfile(version_filename))
            os.remove(version_filename)

    def test_version_setting(self):
        url = '{0}?filename={1}'.format(reverse('fb_versions'),
                                        self.image_name)
        response = self.client.get(url)

        for version in fb_settings.ADMIN_VERSIONS:
            value = os.path.join(self.working_dir, self.image_name)
            version_filename = get_version_path(value, version)

            version_prefix = fb_settings.VERSIONS[version]['verbose_name']
            needle = '<strong>{0}</strong>'.format(version_prefix)
            self.assertInHTML(needle, response.content.decode('utf-8'))

            os.remove(version_filename)
