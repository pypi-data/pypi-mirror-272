import re
import fnmatch
import operator

from .utils import ensure_list


def filter_op_and(filters):
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return lambda value: all(it(value) for it in filters)


def filter_op_or(filters):
    if not filters:
        return None
    if len(filters) == 1:
        return filters[0]
    return lambda value: any(it(value) for it in filters)


def filter_op_not(flt):
    if not flt:
        return
    return lambda value: not flt(value)


def filter_match(val, getter):
    if type(val) is str and len(val) >= 2 and val[0] == '/' and val[-1] == '/':
        r = re.compile(val[1:-1])
        return lambda value: bool(r.search(str(getter(value) or '')))
    else:
        return lambda value: getter(value) == val


def filter_fnmatch(pattern, getter):
    return lambda value: bool(fnmatch.filter(getter(value), pattern))


def make_filter(values, flt_fn, getter):
    if not values:
        return
    return filter_op_or([flt_fn(v, getter) for v in ensure_list(values)])


def update_type_getter(value):
    status = value.props.getProperty('event.change.status')
    if status == 'MERGED':
        return 'merged'
    elif status == 'TAGGED':
        return 'tagged'
    return 'new'


FILTERS = {
    'branch': (filter_match, operator.attrgetter('branch')),
    'branches': (filter_match, operator.attrgetter('branch')),
    'comment': (filter_match, operator.attrgetter('comments')),
    'comments': (filter_match, operator.attrgetter('comments')),
    'file': (filter_fnmatch, operator.attrgetter('files')),
    'files': (filter_fnmatch, operator.attrgetter('files')),
    'status': (filter_match, update_type_getter),
    'tag': (filter_match, lambda value: value.props.getProperty('event.change.tag')),
}


def make_filters(filters, is_or=False):
    if hasattr(filters, 'keys'):
        filters = [filters]

    result = []
    for desc in filters:
        for name, values in desc.items():
            if name in FILTERS:
                fn, getter = FILTERS[name]
                result.append(make_filter(values, fn, getter))
            elif name == 'not':
                result.append(filter_op_not(make_filters(values)))
            elif name == 'or':
                result.append(make_filters(values, True))
            else:
                getter = lambda value: value.props.getProperty(name)
                result.append(make_filter(values, filter_match, getter))

    if is_or:
        return filter_op_or(list(filter(None, result)))
    else:
        return filter_op_and(list(filter(None, result)))
