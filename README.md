# Changelog
It is now possible to integrate with django-suit, django-suit-ckeditor and django-suit-redactor. 

Soon i will put more info.

# Installation

This text was copied from "the django-filebrowser project on [Google Code](http://django-filebrowser.googlecode.com/svn-history/r338/wiki/installationbasic.wiki) and updated for this readme markup and the django-media-manager version.

## Basic Installation
<code>pip install https://github.com/miguelramos/django-media-manager/archive/master.zip</code>

## Install the FileBrowser

Install the FileBrowser anywhere on your python-path. I'm personally using the project-directory.

<pre>git clone https://github.com/miguelramos/django-media-manager.git</pre>


## Copy media

Copy the folder /media either to your admin media directory or to your preferred media directory (in this case, you have to edit URL_FILEBROWSER_MEDIA in fb_settings).

## Add filebrowser to INSTALLED_APPS.

Open your projects settings file (settings.py) and add the filebrowser to INSTALLED_APPS.

## Change fb_settings.py

Either change fb_settings.py or overwrite the filebrowser settings in your project settings file (settings.py). See [Available Settings](http://code.google.com/p/django-filebrowser/wiki/Settings).

_*Note*: You do need an upload directory. The default one is "uploads" inside your MEDIA_ROOT. Check URL_WWW and PATH_SERVER if you change this directory._

## Change your urls.py

Add the following line _before_ the admin URLs:
<pre>(r'^admin/filebrowser/', include('filebrowser.urls')),</pre>

## Add the FileBrowser to your Admin Index page

Edit /templates/admin/index.html and add this code _before_ {% for app in app_list %}:

<pre>{% include 'filebrowser/append.html' %}</pre>

_That's it!_


# Troubleshooting

There are problems with the upload using wsgi version less than 2.4. Make sure you have a more updated version.

About 90% of the problems installing the filebrowser are related to wrong _URLs_ and/or _paths_. So, please read through [Available Settings](http://code.google.com/p/django-filebrowser/wiki/Settings) and check everything with either _URL_ or _path_ carefully (especially when using TinyMCE).