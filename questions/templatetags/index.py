from django import template


register = template.Library()

@register.filter
def truncate_str(string_to_truncate, limit=10):
    if isinstance(string_to_truncate, str) and len(string_to_truncate) > limit + 3:
        return string_to_truncate[:limit] + '...'
    return string_to_truncate

@register.filter
def before(page_obj, pages=11):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    half_pages = pages // 2
    start = page_num - half_pages
    if pages_cnt - page_num < half_pages:
        start -= (half_pages - (pages_cnt - page_num))
    start = max(1, start)
    return list(range(start, page_num))

@register.filter
def after(page_obj, pages=11):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    half_pages = pages // 2
    end = page_num + half_pages
    if page_num <= half_pages:
        end += half_pages + 1 - page_num
    end = min(end, pages_cnt)
    return list(range(page_num + 1, end + 1))