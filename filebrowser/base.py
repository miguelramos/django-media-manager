# coding: utf-8

# imports
import os, re, datetime
from time import gmtime, strftime
from urllib.parse import quote

# django imports
from django.core.files.base import File
from django.conf import settings

# filebrowser imports
from filebrowser.settings import *
from filebrowser.conf import fb_settings
from filebrowser.functions import get_file_type, url_join, is_selectable, get_version_path, url_to_path

# PIL import
if STRICT_PIL:
    from PIL import Image
else:
    try:
        from PIL import Image
    except ImportError:
        import Image


class FileObject(File):
    """
    The FileObject represents a File on the Server.

    PATH has to be relative to MEDIA_ROOT.

    11/1/2014: Now a wrapper around File objects to it can operate as a drop-in replacement for FileFields
    """

    def __init__(self, path, instance=None, field=None, file=None):
        '''
        `os.path.split` Split the pathname path into a pair, (head, tail) where tail is the last pathname component and head is everything leading up to that. The tail part will never contain a slash; if path ends in a slash, tail will be empty. If there is no slash in path, head will be empty. If path is empty, both head and tail are empty.
        '''
        self.instance = instance
        self.field = field
        self.path = path
        self.url_rel = path.replace("\\", "/")
        self.head, self.filename = os.path.split(path)
        # important for sorting
        self.filename_lower = self.filename.lower()
        # strange if file no extension then this folder
        self.filetype = get_file_type(self.filename)
        self.name = self.abspath
        try:
            if self.exists:
                self.file = open(self.abspath, 'rb')
                # img = self.file.read()
                # print(img)
            else:
                self.file = None
        except Exception as ex:
            print(ex)
            pass

    # Here in case of compatibility issues; See below;
    # def __repr__(self):
    #     return self.path

    # def __str__(self):
    #     return self.path

    @property
    def filesize(self):
        """
        Filesize.
        """
        path = (self.path)
        if os.path.isfile(os.path.join(fb_settings.MEDIA_ROOT, path)) or os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, path)):
            return os.path.getsize(os.path.join(fb_settings.MEDIA_ROOT, path))
        return ""

    @property
    def date(self):
        """
        Date.
        """
        if os.path.isfile(os.path.join(fb_settings.MEDIA_ROOT, self.path)) or os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, self.path)):
            return os.path.getmtime(os.path.join(fb_settings.MEDIA_ROOT, self.path))
        return ""

    @property
    def datetime(self):
        """
        Datetime Object.
        """
        return datetime.datetime.fromtimestamp(self.date)

    @property
    def extension(self):
        """
        Extension.
        """
        return "{0}".format(os.path.splitext(self.filename)[1])

    @property
    def filetype_checked(self):
        if self.filetype == "Folder" and os.path.isdir(self.path_full):
            return self.filetype
        elif self.filetype != "Folder" and os.path.isfile(self.path_full):
            return self.filetype
        else:
            return ""

    @property
    def path_full(self):
        """
        Full server PATH including MEDIA_ROOT.
        """
        return os.path.join(fb_settings.MEDIA_ROOT, self.path)

    @property
    def path_relative(self):
        return self.path

    @property
    def path_relative_directory(self):
        """
        Path relative to initial directory.
        """
        directory_re = re.compile(r'^({0})'.format((fb_settings.DIRECTORY)))
        value = directory_re.sub('', self.path)
        return "{0}".format(value)

    @property
    def url_relative(self):
        return self.url_rel

    @property
    def url_full(self):
        """
        Full URL including MEDIA_URL.
        """
        return quote(url_join(fb_settings.MEDIA_URL, self.url_rel), safe='/:')

    @property
    def url(self):
        """
        Full URL including MEDIA_URL.
        """
        return quote(url_join(fb_settings.MEDIA_URL, self.url_rel), safe='/:')

    @property
    def url_save(self):
        """
        URL used for the filebrowsefield.
        """
        if SAVE_FULL_URL:
            return self.url_full
        else:
            return self.url_rel

    @property
    def url_thumbnail(self):
        """
        Thumbnail URL.
        """
        if self.filetype == "Image":
            return "{0}".format(url_join(fb_settings.MEDIA_URL, get_version_path(self.path, ADMIN_THUMBNAIL)))
        else:
            return ""

    def url_admin(self):
        if self.filetype_checked == "Folder":
            directory_re = re.compile(r'^({0})'.format((fb_settings.DIRECTORY)))
            value = directory_re.sub('', self.path)
            return "{0}".format(value)
        else:
            return "{0}".format(url_join(fb_settings.MEDIA_URL, self.path))

    @property
    def dimensions(self):
        """
        Image Dimensions.
        """
        if self.filetype == 'Image':
            try:
                im = Image.open(os.path.join(fb_settings.MEDIA_ROOT, self.path))
                return im.size
            except:
                pass
        else:
            return False

    @property
    def width(self):
        """
        Image Width.
        """
        return self.dimensions[0]

    @property
    def height(self):
        """
        Image Height.
        """
        return self.dimensions[1]

    @property
    def orientation(self):
        """
        Image Orientation.
        """
        if self.dimensions:
            if self.dimensions[0] >= self.dimensions[1]:
                return "Landscape"
            else:
                return "Portrait"
        else:
            return None

    @property
    def is_empty(self):
        """True if Folder is empty, False if not."""
        if os.path.isdir(self.path_full):
            if not os.listdir(self.path_full):
                return True
            else:
                return False
        else:
            return None

    _exists_stored = None

    @property
    def exists(self):
        # print('looking for ' + abs_path)
        "True, if the path exists, False otherwise"
        if self._exists_stored is None:
            self._exists_stored = os.path.exists(self.abspath)
        return self._exists_stored

    _abspath = None

    @property
    def abspath(self):
        if self._abspath is None:
            self._abspath = os.path.abspath(os.path.join(fb_settings.MEDIA_ROOT, self.path))
        return self._abspath

    def __repr__(self):
        return (self.url_save)

    def __str__(self):
        return (self.url_save)

    def __unicode__(self):
        return (self.url_save)
