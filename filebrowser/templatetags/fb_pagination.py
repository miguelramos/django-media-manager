# coding: utf-8
from django.template import Library

from filebrowser.conf import fb_settings

register = Library()

DOT = '.'


def _template():
    if fb_settings.SUIT_TEMPLATE:
        path = 'suit/'
    else:
        path = 'filebrowser/'

    return path


@register.inclusion_tag(
    _template() + 'include/paginator.html', takes_context=True
)
def pagination(context):
    page_num = context['page'].number - 1
    paginator = context['p']
    
    if not paginator.num_pages or paginator.num_pages == 1:
        page_range = []
    else:
        on_each_side = 3
        on_ends = 2
        
        # If there are 10 or fewer pages, display links to every page.
        # Otherwise, do some fancy
        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            # Insert "smart" pagination links, so that there are always ON_ENDS
            # links at either end of the list of pages, and there are always
            # ON_EACH_SIDE links at either end of the "current page" link.
            page_range = []
            if page_num > (on_each_side + on_ends):
                page_range.extend(range(0, on_each_side - 1))
                page_range.append(DOT)
                page_range.extend(
                    range(page_num - on_each_side, page_num + 1)
                )
            else:
                page_range.extend(range(0, page_num + 1))
            if page_num < (paginator.num_pages - on_each_side - on_ends - 1):
                page_range.extend(
                    range(page_num + 1, page_num + on_each_side + 1)
                )
                page_range.append(DOT)
                page_range.extend(
                    range(paginator.num_pages - on_ends, paginator.num_pages)
                )
            else:
                page_range.extend(range(page_num + 1, paginator.num_pages))
    
    return {
        'page_range': page_range,
        'page_num': page_num,
        'results_var': context['results_var'],
        'query': context['query'],
    }
