from .base import BaseTestCase
from filebrowser.forms import MakeDirForm, RenameForm

import os


class FormsTests(BaseTestCase):
    """
    Test forms
    """
    def test_make_dir_form(self):
        data = {'dir_name': 'test_dir%$'}
        form = MakeDirForm(self.working_dir, data)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['dir_name'],
            ['Only letters, numbers, underscores, '
             'spaces and hyphens are allowed.']
        )

        data = {'dir_name': 'test_dir'}
        form = MakeDirForm(self.working_dir, data)
        self.assertTrue(form.is_valid())

        os.makedirs(os.path.join(self.working_dir, 'test_dir'))

        data = {'dir_name': 'test_dir'}
        form = MakeDirForm(self.working_dir, data)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['dir_name'], ['The Folder already exists.']
        )

        os.rmdir(os.path.join(self.working_dir, 'test_dir'))

    def test_rename_form(self):
        data = {'name': 'test_dir%$'}
        file_extension = ''
        form = RenameForm(self.working_dir, file_extension, data)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['name'],
            ['Only letters, numbers, underscores, '
             'spaces and hyphens are allowed.']
        )

        os.makedirs(os.path.join(self.working_dir, 'test_dir'))
        data = {'name': 'test_dir'}
        file_extension = ''
        form = RenameForm(self.working_dir, file_extension, data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['name'], ['The Folder already exists.'])

        os.rmdir(os.path.join(self.working_dir, 'test_dir'))

        file_name, file_extension = self.image_name.split('.')
        data = {'name': file_name}
        form = RenameForm(
            self.working_dir, '.{0}'.format(file_extension), data
        )
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['name'], ['The File already exists.'])
