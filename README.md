# Changelog

### 11-17-2014 v4.0.6
*   Gave FileBrowseField a default max_length of 255. Can be overridden in declaration.
*   Added a `deconstruct` method that is necessary for Django 1.7 migrations.

### 11-17-2014 v4.0.5
*   Made FileBrowseField.js more cautious about wether the "link" DOM object exists.

### 11-13-2014 v4.0.4
*   Bug fix. If value on a FileBrowseField is blank, it's set to '' in the database.

### 11-13-2014 v4.0.3
*   Bug fix. Field now returns None or empty string if blank.

### 11-13-2014 v4.0.2
*   Bug fix. Field should have had `self.file = None` when no file is assigned.

### 11-13-2014 v4.0.1
*   Urls are now encoded properly so they can be output anywhere.
*   `path` property of FileObject is still unencoded to ensure the filename is still available.

### 11-11-2014 v4.0.0
*   BREAKS BACKWARDS COMPATIBILITY: Due to the default that files are stored with
    relative filenames rather than absolute.
*   Uploadify is deprecated; Uses qq uploader now.
*   Still targeting Python 3 only.
*   FileBrowseFields can now integrate with imagekit as it mimics an FileField 
    interface now.

### 25-08-2014 v3.4.0
*   Uses Pillow now.
*   Python 3 only now.

### 02-07-2013
*	Refactor and resolved an issue on window.opener event.
*	Refactor FB_Redactor plugin.

### 28-06-2013

*	Support for django-suit
*	Support for django-suit-ckeditor
*	Support for django-suit-redactor
*	Support for custom user model
*	Mandatory django version higher 1.5

## Basic Installation

	pip install django-media-manager
	or
	pip install git+ssh://git@bitbucket.org:6ft/django-media-manager.git

*	Add filebrowser to INSTALLED_APPS.
*	Add the following line _before_ the admin URLS:
*		(r'^admin/filebrowser/', include('filebrowser.urls'))
*	Collect static files
*	Add __uploads/__ folder to media folder or customize this setting

## Suit support
The application have support for [django-suit](https://github.com/darklow/django-suit) template. To use it add on your settings files the following config:

<code>FILEBROWSER_SUIT_TEMPLATE = True</code> 

Filebrowser will now use templates for django suit.

## Suit CKEditor/Redactor
To use filebrowser on [django-suit-ckeditor](https://github.com/darklow/django-suit-ckeditor) or [django-suit-redactor](https://github.com/darklow/django-suit-redactor) please follow the example bellow:

	#models.py
	
	from django.db import models
	from filebrowser.fields import FileBrowseField
	
	class MediaPublication(models.Model):
    	ckeditor = models.TextField(help_text='Editor CKEditor')
    	redactor = models.TextField(help_text='Editor Redactor')
    	image = FileBrowseField("Image", max_length=200, blank=True, null=True)
    	image_initialdir = FileBrowseField("Image (Initial Directory)", max_length=200, directory="images/", blank=True, null=True)
    	image_extensions = FileBrowseField("Image (Extensions)", max_length=200, extensions=['.jpg'],
                                       help_text="Only jpg-Images allowed.", blank=True, null=True)
    	image_format = FileBrowseField("Image (Format)", max_length=200, format='Image', blank=True, null=True)
    	pdf = FileBrowseField("PDF", max_length=200, directory="documents/", extensions=['.pdf'], format='Document',
                          blank=True, null=True)

    	class Meta:
        	ordering = ['image',]
        	verbose_name = 'publication'
        	verbose_name_plural = 'publications'

To use on admin you need to do some litle tweeks:

	#admin.py
	from django.contrib import admin
	from django.forms import ModelForm, Media
	from suit_ckeditor.widgets import CKEditorWidget
	from suit_redactor.widgets import RedactorWidget

	from .models import MediaPublication


	class Editor(ModelForm):
    	class Meta:
        	widgets = {
            	'ckeditor': CKEditorWidget(editor_options={'startupFocus': True}),
            	'redactor': RedactorWidget(editor_options={
                	'lang': 'en',
                	'plugins': ['filebrowser']
            	}),
        	}

    	class Media:
        	js = ('filebrowser/js/FB_CKEditor.js', 'filebrowser/js/FB_Redactor.js')
        	css = {
            	'all': ('filebrowser/css/suit-filebrowser.css',)
        	}
        	
    class AdminPublication(admin.ModelAdmin):
    	form = Editor

    	fieldsets = (
        	(None, {
            	'classes': ('suit-tab suit-tab-media',),
            	'fields': ['image', 'image_initialdir', 'image_extensions', 'image_format', 'pdf'],
        	}),
        	('CKEditor', {
            	'classes': ('full-width',),
            	'fields': ('ckeditor',)
        	}),
        	('Redactor', {
            	'classes': ('full-width',),
            	'fields': ('redactor',)
        	}),
    	)

    	list_display = ('thumbnail', 'image_extensions', 'pdf')
    	suit_form_tabs = (('media', 'Media'),)

    	def thumbnail(self, obj):
        	if obj.image:
            	return '<img src="%s" />' % obj.image.url_thumbnail
        	else:
            	return ""
    	thumbnail.allow_tags = True


	admin.site.register(MediaPublication, AdminPublication)
   
The most important things are on ModelForm (Media and Widgets). To use browser on CKEditor and have the button to navigate on filebrowser you only need to add the js file to Media

For Redactor you will have to add the plugin option on the widget (plugin name is mandatory - _filebrowser_ ) and add the css and js file to media.

That's it you are now ready to send all kind of files to ckeditor or redactor.

### Screenshots

![](https://dl.dropboxusercontent.com/u/14340361/works/filebrowser.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/filebrowser-versions.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/ckeditor-browser.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/ckeditor-bt-browser.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/ckeditor-image.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/redactor-pop-up.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/redactor-import.jpeg)
![](https://dl.dropboxusercontent.com/u/14340361/works/redactor-files-select.jpeg)

#### TODO

Please this is a work in progress. If you have ideas or want to make it better please fel free to pull requests.

*	Add more options on thumbs sizes


