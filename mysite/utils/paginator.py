from django.core.paginator import Paginator


def paginator_queryset(objs, page_no, num_per_page=5, half_nav_len=5):
    p = Paginator(objs, num_per_page)
    if page_no > p.num_pages:
        page_no = p.num_pages
    if page_no < 1:
        page_no = 1
    page_links = [i for i in range(page_no - half_nav_len, page_no +
        half_nav_len + 1) if i > 0 and i <= p.num_pages]
    page = p.page(page_no)
    previous_link = page_links[0] - 1
    next_link = page_links[-1] + 1
    pagination_data = {"has_previous": page.has_previous(),
                       "has_next": page.has_next(),
                       "previous_link": previous_link,
                       "next_link": next_link,
                       "num_pages": p.num_pages,
                       "page_links": page_links}
    return (page.object_list, pagination_data)
