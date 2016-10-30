# coding: utf-8

# imports
import os
import re
import datetime
from PIL import Image

# filebrowser imports
from filebrowser.settings import SAVE_FULL_URL, ADMIN_THUMBNAIL
from filebrowser.conf import fb_settings
from filebrowser.functions import get_file_type, url_join, get_version_path


class FileObject(object):
    """
    The FileObject represents a File on the Server.
    
    PATH has to be relative to MEDIA_ROOT.
    """
    
    def __init__(self, path):
        """
        `os.path.split` Split the pathname path into a pair, (head, tail)
        where tail is the last pathname component and head is everything
        leading up to that. The tail part will never contain a slash;
        if path ends in a slash, tail will be empty.
        If there is no slash in path, head will be empty.
        If path is empty, both head and tail are empty.
        """
        self.path = path
        self.url_rel = path.replace("\\", "/")
        self.head, self.filename = os.path.split(path)
        # important for sorting
        self.filename_lower = self.filename.lower()
        # strange if file no extension then this folder
        self.filetype = get_file_type(self.filename)
    
    def _filesize(self):
        """
        Filesize.
        """
        path = self.path
        if os.path.isfile(os.path.join(fb_settings.MEDIA_ROOT, path)) or \
                os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, path)):
            return os.path.getsize(os.path.join(fb_settings.MEDIA_ROOT, path))
        return ""
    filesize = property(_filesize)
    
    def _date(self):
        """
        Date.
        """
        if os.path.isfile(os.path.join(fb_settings.MEDIA_ROOT, self.path)) or \
                os.path.isdir(os.path.join(fb_settings.MEDIA_ROOT, self.path)):
            return os.path.getmtime(
                os.path.join(fb_settings.MEDIA_ROOT, self.path)
            )
        return ""
    date = property(_date)
    
    def _datetime(self):
        """
        Datetime Object.
        """
        return datetime.datetime.fromtimestamp(self.date)
    datetime = property(_datetime)
    
    def _extension(self):
        """
        Extension.
        """
        return u"{0}".format(os.path.splitext(self.filename)[1])
    extension = property(_extension)
    
    def _filetype_checked(self):
        if self.filetype == "Folder" and os.path.isdir(self.path_full):
            return self.filetype
        elif self.filetype != "Folder" and os.path.isfile(self.path_full):
            return self.filetype
        else:
            return ""
    filetype_checked = property(_filetype_checked)
    
    def _path_full(self):
        """
        Full server PATH including MEDIA_ROOT.
        """
        return os.path.join(fb_settings.MEDIA_ROOT, self.path)
    path_full = property(_path_full)
    
    def _path_relative(self):
        return self.path
    path_relative = property(_path_relative)
    
    def _path_relative_directory(self):
        """
        Path relative to initial directory.
        """
        directory_re = re.compile(r'^({0})'.format(fb_settings.DIRECTORY))
        value = directory_re.sub('', self.path)
        return value
    path_relative_directory = property(_path_relative_directory)
    
    def _url_relative(self):
        return self.url_rel
    url_relative = property(_url_relative)
    
    def _url_full(self):
        """
        Full URL including MEDIA_URL.
        """
        return url_join(fb_settings.MEDIA_URL, self.url_rel)
    url_full = property(_url_full)
    
    def _url_save(self):
        """
        URL used for the filebrowsefield.
        """
        if SAVE_FULL_URL:
            return self.url_full
        else:
            return self.url_rel
    url_save = property(_url_save)
    
    def _url_thumbnail(self):
        """
        Thumbnail URL.
        """
        if self.filetype == "Image":
            return "{0}".format(
                url_join(
                    fb_settings.MEDIA_URL,
                    get_version_path(self.path, ADMIN_THUMBNAIL)
                )
            )
        else:
            return ""
    url_thumbnail = property(_url_thumbnail)
    
    def url_admin(self):
        if self.filetype_checked == "Folder":
            directory_re = re.compile(r'^({0})'.format(fb_settings.DIRECTORY))
            value = directory_re.sub('', self.path)
            return "{0}".format(value)
        else:
            return "{0}".format(url_join(fb_settings.MEDIA_URL, self.path))
    
    def _dimensions(self):
        """
        Image Dimensions.
        """
        if self.filetype == 'Image':
            try:
                im = Image.open(
                    os.path.join(fb_settings.MEDIA_ROOT, self.path)
                )
                return im.size
            except IOError:
                pass
        else:
            return False
    dimensions = property(_dimensions)
    
    def _width(self):
        """
        Image Width.
        """
        return self.dimensions[0]
    width = property(_width)
    
    def _height(self):
        """
        Image Height.
        """
        return self.dimensions[1]
    height = property(_height)
    
    def _orientation(self):
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
    orientation = property(_orientation)
    
    def _is_empty(self):
        """
        True if Folder is empty, False if not.
        """
        if os.path.isdir(self.path_full):
            if not os.listdir(self.path_full):
                return True
            else:
                return False
        else:
            return None
    is_empty = property(_is_empty)
    
    def __repr__(self):
        return self.url_save
    
    def __str__(self):
        return self.url_save
    
    def __unicode__(self):
        return self.url_save
