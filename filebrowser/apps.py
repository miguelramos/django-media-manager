from django.apps import AppConfig
from django.views.decorators.cache import never_cache
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from filebrowser.conf import fb_settings


class FilebrowserAppConfig(AppConfig):
    name = 'filebrowser'

    def ready(self):
        from django.contrib import admin
        from django.contrib.admin import sites

        class FilebrowserAdminSite(admin.AdminSite):
            @never_cache
            def index(self, request, extra_context=None):
                resp = super(FilebrowserAdminSite, self).index(request,
                                                               extra_context)
                app_dict = {
                    'app_url': reverse('fb_browse'),
                    'models': [
                        {
                            'admin_url': reverse('fb_browse'),
                            'name': 'Browse',
                            'add_url': None
                        },
                        {
                            'admin_url': reverse('fb_mkdir'),
                            'name': _('New Folder'),
                            'add_url': None
                        },
                        {
                            'admin_url': reverse('fb_upload'),
                            'name': _('Upload'),
                            'add_url': None
                        }
                    ],
                    'has_module_perms': True,
                    'name': _('Filebrowser'),
                    'app_label': 'filebrowser'
                }
                resp.context_data['app_list'].append(app_dict)
                return resp

        if fb_settings.SHOW_AT_ADMIN_PANEL:
            fb = FilebrowserAdminSite()
            admin.site = fb
            sites.site = fb
