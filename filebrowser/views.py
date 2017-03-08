# coding: utf-8

# general imports
import os
import re
import mimetypes

# django imports
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_str
from django.conf import settings
from django import forms
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.core.files.move import file_move_safe
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.dispatch import Signal

# filebrowser imports
from filebrowser.settings import (
    EXCLUDE, VERSIONS, EXTENSION_LIST, EXTENSIONS, SELECT_FORMATS,
    DEFAULT_SORTING_BY, DEFAULT_SORTING_ORDER, LIST_PER_PAGE
)
from filebrowser.conf import fb_settings
from filebrowser.functions import (
    path_to_url, sort_by_attr, get_path, get_file, get_version_path,
    get_breadcrumbs, get_filterdate, get_settings_var, handle_file_upload,
    convert_filename, _template
)
from filebrowser.templatetags.fb_tags import query_helper
from filebrowser.base import FileObject
from filebrowser.forms import MakeDirForm, RenameForm

# Precompile regular expressions
filter_re = []
for exp in EXCLUDE:
    filter_re.append(re.compile(exp))
for k, v in VERSIONS.items():
    exp = r'_{0}({1})'.format(k, '|'.join(EXTENSION_LIST))
    filter_re.append(re.compile(exp))


def _check_access(request, *path):
    """
    Return absolute file path if access allow or raise exception.
    """
    abs_path = os.path.abspath(os.path.join(
        fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY, *path))
    if not abs_path.startswith(os.path.abspath(os.path.join(
            fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY))):
        # cause any attempt to leave media root directory to fail
        raise Http404
    return abs_path


@never_cache
@staff_member_required
def browse(request):
    """
    Browse Files/Directories.
    """
    # QUERY / PATH CHECK
    query = request.GET.copy()
    path = get_path(query.get('dir', ''))
    directory = get_path('')

    if 'pop' in query:
        is_popup = True
    else:
        is_popup = False

    if path is not None:
        abs_path = _check_access(request, path)

    if path is None:
        msg = _('The requested Folder does not exist.')
        messages.warning(request, message=msg)
        if directory is None:
            # The DIRECTORY does not exist,
            # raise an error to prevent eternal redirecting.
            raise ImproperlyConfigured(
                _("Error finding Upload-Folder. Maybe it does not exist?"))
        redirect_url = reverse("fb_browse") + query_helper(query, "", "dir")
        return HttpResponseRedirect(redirect_url)

    # INITIAL VARIABLES
    results_var = {'results_total': 0, 'results_current': 0, 'delete_total': 0,
                   'images_total': 0, 'select_total': 0}
    counter = {}
    for k, v in EXTENSIONS.items():
        counter[k] = 0

    dir_list = os.listdir(abs_path)
    files = []
    for file in dir_list:

        # EXCLUDE FILES MATCHING VERSIONS_PREFIX OR ANY OF THE EXCLUDE PATTERNS
        filtered = file.startswith('.')
        for re_prefix in filter_re:
            if re_prefix.search(file):
                filtered = True
        if filtered:
            continue
        results_var['results_total'] += 1

        # CREATE FILEOBJECT
        fileobject = FileObject(
            os.path.join(fb_settings.DIRECTORY, path, file))

        # FILTER / SEARCH
        append = False
        if fileobject.filetype == request.GET.get('filter_type', fileobject.filetype) and \
                get_filterdate(request.GET.get('filter_date', ''), fileobject.date):
            append = True
        if request.GET.get('q') and not re.compile(
                request.GET.get('q').lower(), re.M).search(file.lower()):
            append = False

        # APPEND FILE_LIST
        if append:
            _type = query.get('type')
            try:
                # COUNTER/RESULTS
                if fileobject.filetype == 'Image':
                    results_var['images_total'] += 1
                if fileobject.filetype != 'Folder':
                    results_var['delete_total'] += 1
                elif fileobject.filetype == 'Folder' and fileobject.is_empty:
                    results_var['delete_total'] += 1
                if _type and _type in SELECT_FORMATS and \
                        fileobject.filetype in SELECT_FORMATS[_type]:
                    results_var['select_total'] += 1
                elif not _type:
                    results_var['select_total'] += 1
            except OSError:
                # Ignore items that have problems
                continue
            else:
                files.append(fileobject)
                results_var['results_current'] += 1

        # COUNTER/RESULTS
        if fileobject.filetype:
            counter[fileobject.filetype] += 1

    # SORTING
    query['o'] = request.GET.get('o', DEFAULT_SORTING_BY)
    query['ot'] = request.GET.get('ot', DEFAULT_SORTING_ORDER)
    files = sort_by_attr(files, request.GET.get('o', DEFAULT_SORTING_BY))
    if not request.GET.get(
            'ot') and DEFAULT_SORTING_ORDER == "desc" or request.GET.get(
            'ot') == "desc":
        files.reverse()

    p = Paginator(files, LIST_PER_PAGE)
    try:
        page_nr = int(request.GET.get('p', '1'))
    except ValueError:
        page_nr = 1
    try:
        page = p.page(page_nr)
    except (EmptyPage, InvalidPage):
        page = p.page(p.num_pages)

    return render(request, _template() + 'index.html', {
        'dir': path,
        'p': p,
        'page': page,
        'results_var': results_var,
        'counter': counter,
        'query': query,
        'title': _(u'FileBrowser'),
        'settings_var': get_settings_var(),
        'breadcrumbs': get_breadcrumbs(query, path),
        'breadcrumbs_title': "",
        'is_popup': is_popup
    })


# mkdir signals
filebrowser_pre_createdir = Signal(providing_args=["path", "dirname"])
filebrowser_post_createdir = Signal(providing_args=["path", "dirname"])


@never_cache
@staff_member_required
def mkdir(request):
    """
    Make Directory.
    """
    # QUERY / PATH CHECK
    query = request.GET
    path = get_path(query.get('dir', ''))

    if 'pop' in query:
        is_popup = True
    else:
        is_popup = False

    if path is None:
        msg = _('The requested Folder does not exist.')
        messages.warning(request, message=msg)
        return HttpResponseRedirect(reverse("fb_browse"))
    abs_path = _check_access(request, path)

    if request.method == 'POST':
        form = MakeDirForm(abs_path, request.POST)
        if form.is_valid():
            _new_dir_name = form.cleaned_data['dir_name']
            server_path = _check_access(request, path, _new_dir_name)
            try:
                # PRE CREATE SIGNAL
                filebrowser_pre_createdir.send(sender=request,
                                               path=path,
                                               dirname=_new_dir_name)
                # CREATE FOLDER
                os.mkdir(server_path)
                os.chmod(server_path, 0o775)
                # POST CREATE SIGNAL
                filebrowser_post_createdir.send(sender=request, path=path,
                                                dirname=_new_dir_name)
                # MESSAGE & REDIRECT
                msg = _('The Folder {0} was successfully created.').format(
                    _new_dir_name)
                messages.success(request, message=msg)
                # on redirect, sort by date desc to see
                # the new directory on top of the list
                # remove filter in order to actually _see_ the new folder
                # remove pagination
                redirect_url = reverse("fb_browse") + query_helper(query,
                                                                   "ot=desc,o=date",
                                                                   "ot,o,filter_type,filter_date,q,p")
                return HttpResponseRedirect(redirect_url)
            except OSError as e:
                if e.errno == 13:
                    form.errors['dir_name'] = forms.utils.ErrorList(
                        [_('Permission denied.')])
                else:
                    form.errors['dir_name'] = forms.utils.ErrorList(
                        [_('Error creating folder.')])
    else:
        form = MakeDirForm(abs_path)

    return render(request, _template() + 'makedir.html', {
        'form': form,
        'query': query,
        'title': _(u'New Folder'),
        'settings_var': get_settings_var(),
        'breadcrumbs': get_breadcrumbs(query, path),
        'breadcrumbs_title': _(u'New Folder'),
        'is_popup': is_popup
    })


@never_cache
@staff_member_required
def upload(request):
    """
    Multipe File Upload.
    """

    # QUERY / PATH CHECK
    query = request.GET
    path = get_path(query.get('dir', ''))

    if 'pop' in query:
        is_popup = True
    else:
        is_popup = False

    if path is None:
        msg = _('The requested Folder does not exist.')
        messages.warning(request, message=msg)
        return HttpResponseRedirect(reverse("fb_browse"))
    abs_path = _check_access(request, path)

    # SESSION (used for flash-uploading)
    session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)

    # we need max. upload size in MB for dropzone library
    max_upload_size = fb_settings.MAX_UPLOAD_SIZE / 1048576.0

    # we need accepted files mime-type for dropzone library
    accepted_files = set()
    for ext_list in fb_settings.EXTENSIONS.values():
        for ext in ext_list:
            try:
                accepted_files.add(mimetypes.types_map[ext])
            except KeyError:
                pass

    return render(request, _template() + 'upload.html', {
        'query': query,
        'title': _(u'Select files to upload'),
        'settings_var': get_settings_var(),
        'session_key': session_key,
        'breadcrumbs': get_breadcrumbs(query, path),
        'breadcrumbs_title': _(u'Upload'),
        'is_popup': is_popup,
        'max_upload_size': max_upload_size,
        'accepted_files': ','.join(accepted_files)
    })


@csrf_exempt
@staff_member_required
def _check_file(request):
    """
    Check if file already exists on the server.
    """

    folder = request.GET.get('folder')
    fb_uploadurl_re = re.compile(r'^.*({0})'.format(reverse("fb_upload")))
    folder = fb_uploadurl_re.sub('', folder)
    success = True

    if request.method == 'POST':
        for k, v in request.POST.items():
            if k != "folder":
                v = convert_filename(v)
                if os.path.isfile(
                        smart_str(_check_access(request, folder, v))):
                    success = False
                    break

    return JsonResponse({'success': success})


# upload signals
filebrowser_pre_upload = Signal(providing_args=["path", "file"])
filebrowser_post_upload = Signal(providing_args=["path", "file"])


@csrf_exempt
@staff_member_required
def _upload_file(request):
    """
    Upload file to the server.
    """

    if request.method == 'POST':
        folder = request.GET.get('folder')
        fb_uploadurl_re = re.compile(r'^.*({0})'.format(reverse("fb_upload")))
        folder = fb_uploadurl_re.sub('', folder)
        abs_path = _check_access(request, folder)
        if request.FILES:
            filedata = request.FILES['file']
            filedata.name = convert_filename(filedata.name)
            _check_access(request, abs_path, filedata.name)
            # PRE UPLOAD SIGNAL
            filebrowser_pre_upload.send(sender=request,
                                        path=request.GET.get('folder'),
                                        file=filedata)
            # HANDLE UPLOAD
            uploadedfile = handle_file_upload(abs_path, filedata)
            # MOVE UPLOADED FILE
            # if file already exists
            if os.path.isfile(smart_str(
                    os.path.join(fb_settings.MEDIA_ROOT, fb_settings.DIRECTORY,
                                 folder, filedata.name))):
                old_file = smart_str(os.path.join(abs_path, filedata.name))
                new_file = smart_str(os.path.join(abs_path, uploadedfile))
                file_move_safe(new_file, old_file)
            # POST UPLOAD SIGNAL
            filebrowser_post_upload.send(sender=request,
                                         path=request.GET.get('folder'),
                                         file=FileObject(smart_str(
                                             os.path.join(
                                                 fb_settings.DIRECTORY, folder,
                                                 filedata.name))))
    return JsonResponse({'success': True})


# delete signals
filebrowser_pre_delete = Signal(providing_args=["path", "filename"])
filebrowser_post_delete = Signal(providing_args=["path", "filename"])


@never_cache
@staff_member_required
def delete(request):
    """
    Delete existing File/Directory.

    When trying to delete a Directory, the Directory has to be empty.
    """

    # QUERY / PATH CHECK
    query = request.GET
    path = get_path(query.get('dir', ''))
    filename = get_file(query.get('dir', ''), query.get('filename', ''))
    if path is None or filename is None:
        if path is None:
            msg = _('The requested Folder does not exist.')
        else:
            msg = _('The requested File does not exist.')
        messages.warning(request, message=msg)
        return HttpResponseRedirect(reverse("fb_browse"))
    abs_path = _check_access(request, path)

    msg = ""
    if request.GET:
        if request.GET.get('filetype') != "Folder":
            relative_server_path = os.path.join(fb_settings.DIRECTORY, path,
                                                filename)
            try:
                # PRE DELETE SIGNAL
                filebrowser_pre_delete.send(sender=request, path=path,
                                            filename=filename)

                # DELETE FILE
                os.unlink(smart_str(_check_access(request, path, filename)))
                # DELETE IMAGE VERSIONS/THUMBNAILS
                for version in VERSIONS:
                    try:
                        os.unlink(os.path.join(fb_settings.MEDIA_ROOT,
                                               get_version_path(
                                                   relative_server_path,
                                                   version)))
                    except:
                        pass

                # POST DELETE SIGNAL
                filebrowser_post_delete.send(sender=request, path=path,
                                             filename=filename)
                # MESSAGE & REDIRECT
                msg = _('The file {0} was successfully deleted.').format(
                    filename.lower())
                messages.success(request, message=msg)
                redirect_url = reverse("fb_browse") + query_helper(query, "",
                                                                   "filename,filetype")
                return HttpResponseRedirect(redirect_url)
            except OSError as e:
                # todo: define error message
                msg = str(e)
        else:
            try:
                # PRE DELETE SIGNAL
                filebrowser_pre_delete.send(sender=request, path=path,
                                            filename=filename)
                # DELETE FOLDER
                os.rmdir(_check_access(request, path, filename))
                # POST DELETE SIGNAL
                filebrowser_post_delete.send(sender=request, path=path,
                                             filename=filename)
                # MESSAGE & REDIRECT
                msg = _('The folder {0} was successfully deleted.').format(
                    filename.lower())
                messages.success(request, message=msg)
                redirect_url = reverse("fb_browse") + query_helper(query, "",
                                                                   "filename,filetype")
                return HttpResponseRedirect(redirect_url)
            except OSError as e:
                # todo: define error message
                msg = str(e)

    if msg:
        messages.error(request, e)

    redirect_url = reverse("fb_browse") + query_helper(query, "",
                                                       "filename,filetype")
    return HttpResponseRedirect(redirect_url)


# rename signals
filebrowser_pre_rename = Signal(
    providing_args=["path", "filename", "new_filename"])
filebrowser_post_rename = Signal(
    providing_args=["path", "filename", "new_filename"])


@never_cache
@staff_member_required
def rename(request):
    """
    Rename existing File/Directory.

    Includes renaming existing Image Versions/Thumbnails.
    """
    # QUERY / PATH CHECK
    query = request.GET
    path = get_path(query.get('dir', ''))

    if 'pop' in query:
        is_popup = True
    else:
        is_popup = False

    filename = get_file(query.get('dir', ''), query.get('filename', ''))
    if path is None or filename is None:
        if path is None:
            msg = _('The requested Folder does not exist.')
        else:
            msg = _('The requested File does not exist.')
        messages.warning(request, message=msg)
        return HttpResponseRedirect(reverse("fb_browse"))
    abs_path = _check_access(request, path)
    file_extension = os.path.splitext(filename)[1].lower()

    if request.method == 'POST':
        form = RenameForm(abs_path, file_extension, request.POST)
        if form.is_valid():
            relative_server_path = os.path.join(fb_settings.DIRECTORY, path,
                                                filename)
            new_filename = form.cleaned_data['name'] + file_extension
            new_relative_server_path = os.path.join(fb_settings.DIRECTORY,
                                                    path, new_filename)
            try:
                # PRE RENAME SIGNAL
                filebrowser_pre_rename.send(sender=request, path=path,
                                            filename=filename,
                                            new_filename=new_filename)
                # DELETE IMAGE VERSIONS/THUMBNAILS
                # regenerating versions/thumbs will be done automatically
                for version in VERSIONS:
                    try:
                        os.unlink(os.path.join(fb_settings.MEDIA_ROOT,
                                               get_version_path(
                                                   relative_server_path,
                                                   version)))
                    except:
                        pass
                # RENAME ORIGINAL
                os.rename(
                    os.path.join(fb_settings.MEDIA_ROOT, relative_server_path),
                    os.path.join(fb_settings.MEDIA_ROOT,
                                 new_relative_server_path))
                # POST RENAME SIGNAL
                filebrowser_post_rename.send(sender=request, path=path,
                                             filename=filename,
                                             new_filename=new_filename)
                # MESSAGE & REDIRECT
                msg = _('Renaming was successful.')
                messages.success(request, message=msg)
                redirect_url = reverse("fb_browse") + query_helper(query, "",
                                                                   "filename")
                return HttpResponseRedirect(redirect_url)
            except OSError as e:
                form.errors['name'] = forms.utils.ErrorList([_('Error.')])
    else:
        form = RenameForm(abs_path, file_extension)

    return render(request, _template() + 'rename.html', {
        'form': form,
        'query': query,
        'file_extension': file_extension,
        'title': _(u'Rename "{0}"').format(filename),
        'settings_var': get_settings_var(),
        'breadcrumbs': get_breadcrumbs(query, path),
        'breadcrumbs_title': _(u'Rename'),
        'is_popup': is_popup
    })


@never_cache
@staff_member_required
def versions(request):
    """
    Show all Versions for an Image according to ADMIN_VERSIONS.
    """

    # QUERY / PATH CHECK
    query = request.GET
    path = get_path(query.get('dir', ''))

    if 'pop' in query:
        is_popup = True
    else:
        is_popup = False

    filename = get_file(query.get('dir', ''), query.get('filename', ''))
    if path is None or filename is None:
        if path is None:
            msg = _('The requested Folder does not exist.')
        else:
            msg = _('The requested File does not exist.')
        messages.warning(request, message=msg)
        return HttpResponseRedirect(reverse("fb_browse"))
    abs_path = _check_access(request, path)

    return render(request, _template() + 'versions.html', {
        'original': path_to_url(
            os.path.join(fb_settings.DIRECTORY, path, filename)),
        'query': query,
        'title': _(u'Versions for "{0}"').format(filename),
        'settings_var': get_settings_var(),
        'breadcrumbs': get_breadcrumbs(query, path),
        'breadcrumbs_title': _(u'Versions for "{0}"').format(filename),
        'is_popup': is_popup
    })
