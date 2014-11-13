# coding: utf-8

# imports
import os


# django imports
from django.db import models
from django import forms
from django.forms.widgets import Input
from django.core.files.base import File
from django.db.models.fields import Field, CharField
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

# filebrowser imports
from filebrowser.settings import *
from filebrowser.base import FileObject
from filebrowser.conf import fb_settings
from filebrowser.functions import url_to_path


def _template():
    if fb_settings.SUIT_TEMPLATE:
        path = 'suit/'
    else:
        path = 'filebrowser/'

    return path


class FileBrowseWidget(Input):
    input_type = 'text'

    class Media:
        js = (os.path.join(URL_FILEBROWSER_MEDIA, 'js/AddFileBrowser.js'), )
        css = {
            'all': (
                os.path.join(URL_FILEBROWSER_MEDIA, 'css/filebrowser.css'),
                os.path.join(URL_FILEBROWSER_MEDIA, 'css/suit-filebrowser.css'),
            )
        }

    def __init__(self, attrs=None):
        self.directory = attrs.get('directory', '')
        self.extensions = attrs.get('extensions', '')
        self.format = attrs.get('format', '')
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {}

    def render(self, name, value, attrs=None):
        if value is None:
            value = ""
        elif not isinstance(value, FileObject):
            value = FileObject(value)
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        final_attrs['search_icon'] = URL_FILEBROWSER_MEDIA + 'img/filebrowser_icon_show.gif'
        final_attrs['directory'] = self.directory
        final_attrs['extensions'] = self.extensions
        final_attrs['format'] = self.format
        final_attrs['ADMIN_THUMBNAIL'] = ADMIN_THUMBNAIL
        final_attrs['DEBUG'] = DEBUG
        if value != "":
            try:
                final_attrs['directory'] = os.path.split(value.path_relative_directory)[0]
            except:
                pass
        return render_to_string(_template() + "custom_field.html", locals())


class FileBrowseFormField(forms.CharField):
    widget = FileBrowseWidget

    default_error_messages = {
        'extension': _('Extension {0} is not allowed. Only {1} is allowed.'),
    }

    def __init__(self, max_length=None, min_length=None,
                 directory=None, extensions=None, format=None,
                 *args, **kwargs):
        self.max_length, self.min_length = max_length, min_length
        self.directory = directory
        self.extensions = extensions
        if format:
            self.format = format or ''
            self.extensions = extensions or EXTENSIONS.get(format)
        super(FileBrowseFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = super(FileBrowseFormField, self).clean(value)
        if value == '':
            return value
        file_extension = os.path.splitext(value)[1].lower()
        if self.extensions and not file_extension in self.extensions:
            raise forms.ValidationError(self.error_messages['extension'].format(file_extension, ", ".join(self.extensions)))
        return value


class FileObjectDescriptor(object):
    def __init__(self, field):
        self.field = field

    def __get__(self, instance=None, owner=None):
        if instance is None:
            raise AttributeError(
                "The '%s' attribute can only be accessed from %s instances."
                % (self.field.name, owner.__name__))

        # This is slightly complicated, so worth an explanation.
        # instance.file`needs to ultimately return some instance of `File`,
        # probably a subclass. Additionally, this returned object needs to have
        # the FieldFile API so that users can easily do things like
        # instance.file.path and have that delegated to the file storage engine.
        # Easy enough if we're strict about assignment in __set__, but if you
        # peek below you can see that we're not. So depending on the current
        # value of the field we have to dynamically construct some sort of
        # "thing" to return.

        # The instance dict contains whatever was originally assigned
        # in __set__.
        file = instance.__dict__[self.field.name]
        # print(file)

        # if it's none, return none
        if file is None or (isinstance(file, str) and len(file) == 0):
            return instance.__dict__[self.field.name]

        # If this value is a string (instance.file = "path/to/file") or None
        # then we simply wrap it with the appropriate attribute class according
        # to the file field. [This is FieldFile for FileFields and
        # ImageFieldFile for ImageFields; it's also conceivable that user
        # subclasses might also want to subclass the attribute class]. This
        # object understands how to convert a path to a file, and also how to
        # handle None.
        if isinstance(file, str) and file is not None:
            attr = self.field.attr_class(file, instance=instance, field=self.field)
            instance.__dict__[self.field.name] = attr

        # Other types of files may be assigned as well, but they need to have
        # the FieldFile interface added to the. Thus, we wrap any other type of
        # File inside a FieldFile (well, the field's attr_class, which is
        # usually FieldFile).
        elif isinstance(file, File) and not isinstance(file, FileObject):
            file_copy = self.field.attr_class(file.name, instance=instance, field=self.field)
            file_copy.file = file
            file_copy._committed = False
            instance.__dict__[self.field.name] = file_copy

        # Finally, because of the (some would say boneheaded) way pickle works,
        # the underlying FieldFile might not actually itself have an associated
        # file. So we need to reset the details of the FieldFile in those cases.
        elif isinstance(file, FileObject) and not hasattr(file, 'field'):
            file.instance = instance
            file.field = self.field
            # file.storage = self.field.storage

        # That was fun, wasn't it?
        return instance.__dict__[self.field.name]

    def __set__(self, instance, value):
        instance.__dict__[self.field.name] = value


class FileBrowseField(Field):
    __metaclass__ = models.SubfieldBase
    attr_class = FileObject
    descriptor_class = FileObjectDescriptor

    def __init__(self, *args, **kwargs):
        self.directory = kwargs.pop('directory', '')
        self.extensions = kwargs.pop('extensions', '')
        self.format = kwargs.pop('format', '')
        super(FileBrowseField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(FileBrowseField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self.descriptor_class(self))

    def to_python(self, value):
        if not value or isinstance(value, FileObject):
            return value
        return FileObject(url_to_path(value))

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        return value.path

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        if not value:
            return value
        return value.path

    def get_prep_value(self, value):
        if not value:
            return value
        return value.path

    def get_manipulator_field_objs(self):
        return [oldforms.TextField]

    def get_internal_type(self):
        return "CharField"

    def formfield(self, **kwargs):
        attrs = {}
        attrs["directory"] = self.directory
        attrs["extensions"] = self.extensions
        attrs["format"] = self.format
        defaults = {
            'form_class': FileBrowseFormField,
            'widget': FileBrowseWidget(attrs=attrs),
            'directory': self.directory,
            'extensions': self.extensions,
            'format': self.format
        }
        defaults.update(kwargs)
        return super(FileBrowseField, self).formfield(**defaults)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^filebrowser\.fields\.FileBrowseField"])
except:
    pass
