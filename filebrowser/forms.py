# coding: utf-8

# imports
import re
import os

# django imports
from django import forms
from django.utils.translation import ugettext as _

# filebrowser imports
from filebrowser.settings import FOLDER_REGEX
from filebrowser.functions import convert_filename

alnum_name_re = re.compile(FOLDER_REGEX)


class MakeDirForm(forms.Form):
    """
    Form for creating Folder.
    """
    dir_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'vTextField', 'max_length': 50, 'min_length': 3}
        ),
        label=_('Name'),
        help_text=_('Only letters, numbers, underscores, '
                    'spaces and hyphens are allowed.'),
        required=True
    )

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(MakeDirForm, self).__init__(*args, **kwargs)
    
    def clean_dir_name(self):
        # only letters, numbers, underscores,
        # spaces and hyphens are allowed.
        if not alnum_name_re.search(self.cleaned_data['dir_name']):
            raise forms.ValidationError(
                _('Only letters, numbers, underscores, '
                  'spaces and hyphens are allowed.')
            )
        # Folder must not already exist.
        if os.path.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['dir_name']))):
            raise forms.ValidationError(_('The Folder already exists.'))
        return convert_filename(self.cleaned_data['dir_name'])


class RenameForm(forms.Form):
    """
    Form for renaming Folder/File.
    """
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'vTextField', 'max_length': 50, 'min_length': 3}
        ),
        label=_('New Name'),
        help_text=_('Only letters, numbers, underscores, '
                    'spaces and hyphens are allowed.'),
        required=True
    )

    def __init__(self, path, file_extension, *args, **kwargs):
        self.path = path
        self.file_extension = file_extension
        super(RenameForm, self).__init__(*args, **kwargs)
    
    def clean_name(self):
        if self.cleaned_data['name']:
            # only letters, numbers, underscores,
            # spaces and hyphens are allowed.
            if not alnum_name_re.search(self.cleaned_data['name']):
                raise forms.ValidationError(
                    _('Only letters, numbers, underscores, '
                      'spaces and hyphens are allowed.')
                )
            #  folder/file must not already exist.
            if os.path.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))):
                raise forms.ValidationError(_('The Folder already exists.'))
            elif os.path.isfile(os.path.join(self.path, convert_filename(self.cleaned_data['name']) + self.file_extension)):
                raise forms.ValidationError(_('The File already exists.'))
        return convert_filename(self.cleaned_data['name'])
