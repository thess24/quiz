from django import template

register = template.Library()

@register.filter
def sort_by_reverse(items, attr):
    """
    General sort filter - sorts by either attribute or key.
    """
    def key_func(item):
        try:
            return getattr(item, attr)
        except AttributeError:
            try:
                return item[attr]
            except TypeError:
                getattr(item, attr)  # Reraise AttributeError
    return sorted(items, key=key_func, reverse=True)