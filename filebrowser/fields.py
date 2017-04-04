# coding: utf-8

# imports
import os

# django imports
from django import forms
from django.forms.widgets import Input
from django.db.models.fields import Field
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# filebrowser imports
from filebrowser.settings import (
    URL_FILEBROWSER_MEDIA, ADMIN_THUMBNAIL, DEBUG, EXTENSIONS, MEDIA_ROOT,
    DIRECTORY
)
from filebrowser.base import FileObject
from filebrowser.functions import url_to_path, _template


class FileBrowseWidget(Input):
    input_type = 'text'

    class Media:
        js = (os.path.join(URL_FILEBROWSER_MEDIA, 'js/AddFileBrowser.js'),)

    def __init__(self, attrs=None):
        self.directory = attrs.get('directory', '')
        self.extensions = attrs.get('extensions', '')
        self.format = attrs.get('format', '')
        super(FileBrowseWidget, self).__init__(attrs)
        # if field have a directory - create it
        dir_path = os.path.join(MEDIA_ROOT, DIRECTORY, self.directory)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['search_icon'] = os.path.join(
            URL_FILEBROWSER_MEDIA, 'img/filebrowser_icon_show.gif'
        )
        final_attrs['directory'] = self.directory
        final_attrs['extensions'] = self.extensions
        final_attrs['format'] = self.format
        final_attrs['ADMIN_THUMBNAIL'] = ADMIN_THUMBNAIL
        final_attrs['DEBUG'] = DEBUG
        if value != "":
            try:
                final_attrs['directory'] = \
                os.path.split(value.path_relative_directory)[0]
            except:
                pass
        return render_to_string(_template() + "custom_field.html", locals())


class FileBrowseFormField(forms.CharField):
    default_error_messages = {
        'extension': _(
            u'Extension %(ext)s is not allowed. Only %(allowed)s is allowed.'),
    }

    def __init__(self, max_length=None, min_length=None,
                  extensions=None, format=None, *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        self.directory = kwargs.pop('directory', '')
        self.extensions = extensions
        self.format = format or ''
        self.extensions = extensions or EXTENSIONS.get(format)

        attrs = {
            "directory": self.directory,
            "extensions": self.extensions,
            "format": self.format
        }
        self.widget = FileBrowseWidget(attrs)
        super(FileBrowseFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(FileBrowseFormField, self).clean(value)
        if value == '':
            return value
        file_extension = os.path.splitext(value)[1].lower()
        if self.extensions and file_extension not in self.extensions:
            raise forms.ValidationError(
                self.error_messages['extension'] % {'ext': file_extension,
                                                    'allowed': ", ".join(
                                                        self.extensions)})
        return value


class FileBrowseField(Field):
    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop('directory', '')
        self.extensions = kwargs.pop('extensions', '')
        self.format = kwargs.pop('format', '')
        kwargs['max_length'] = kwargs.get('max_length', 200)
        super(FileBrowseField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection, context):
        if not value or isinstance(value, FileObject):
            return value
        return FileObject(url_to_path(value))

    def to_python(self, value):
        if not value or isinstance(value, FileObject):
            return value
        return FileObject(url_to_path(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return str(value)

    # FIXME: recheck or need it
    # @staticmethod
    # def get_manipulator_field_objs():
    #     return [oldforms.TextField]

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        attrs = {
            "directory": self.directory,
            "extensions": self.extensions,
            "format": self.format
        }
        defaults = {
            'form_class': FileBrowseFormField,
            'widget': FileBrowseWidget(attrs=attrs),
            'directory': self.directory,
            'extensions': self.extensions,
            'format': self.format
        }
        defaults.update(kwargs)
        return super(FileBrowseField, self).formfield(**defaults)
