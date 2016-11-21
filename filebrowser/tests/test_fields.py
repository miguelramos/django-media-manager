from django import forms
from django.db import connection

from .base import BaseTestCase
from filebrowser.fields import FileBrowseFormField, FileBrowseField


class FieldsTests(BaseTestCase):
    """
    Test fields and widgets
    """
    def test_form_field(self):
        class TestForm(forms.Form):
            image = FileBrowseFormField(format='Image', extensions=['.jpg'])

        data = {'image': 'test.txt'}
        form = TestForm(data)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['image'],
            ['Extension .txt is not allowed. Only .jpg is allowed.']
        )

        data = {'image': self.image_name}
        form = TestForm(data)
        self.assertTrue(form.is_valid())

    def test_model_field(self):
        f = FileBrowseField()
        self.assertEqual(f.db_parameters(connection)['type'], 'varchar(200)')
