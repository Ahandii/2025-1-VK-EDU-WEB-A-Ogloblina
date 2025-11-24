from django import template


register = template.Library()

@register.filter
def truncate_str(string_to_truncate, limit=10):
    if isinstance(string_to_truncate, str) and len(string_to_truncate) > limit + 3:
        return string_to_truncate[:limit] + '...'
    return string_to_truncate

@register.filter
def first(page_obj, k=3):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    if pages_cnt <= 2 * k:
        return list(range(1, pages_cnt))
    return [1] if pages_cnt > 0 else []

@register.filter
def middle(page_obj, k=3):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    if pages_cnt <= 2 * k:
        return []
    start = max(2, page_num - (k - 1) // 2)
    end = min(pages_cnt - 1, start + k - 1)
    start = max(2, end - k + 1)
    return list(range(start, end + 1))

@register.filter
def last(page_obj, k=3):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    
    if pages_cnt > 1:
        return [pages_cnt]
    return []

@register.filter
def show_first_dots(page_obj, k=3):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    
    if pages_cnt <= k + 2:
        return False
    
    middle_pages = middle(page_obj, k)
    if not middle_pages:
        return False
    return middle_pages[0] > 2

@register.filter
def show_last_dots(page_obj, k=3):
    page_num = page_obj.number
    pages_cnt = page_obj.paginator.num_pages
    
    if pages_cnt <= k + 2:
        return False
    
    middle_pages = middle(page_obj, k)
    if not middle_pages:
        return False
    return middle_pages[-1] < pages_cnt - 1