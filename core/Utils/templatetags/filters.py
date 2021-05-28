import json
import os
import re
from decimal import Decimal
from urllib.parse import unquote

from django import template
from django.conf import settings
from django.template import Node
from django.template.defaultfilters import stringfilter
from django.utils import formats, timezone
from django.utils.html import conditional_escape
from django.utils.text import Truncator
from django_hosts.resolvers import reverse
import pytz


register = template.Library()


def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places  # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = list(map(str, digits))
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def money_default_fmt(value, places=0, dp='', curr='$', sep=',', pos=''):
    if value is None or value == '':
        return ''
    return moneyfmt(value, places=places, curr=curr, sep=sep, dp=dp, pos=pos)


@register.filter
@stringfilter
def money_frm(value, args=None):
    if not value or value == 'None':
        return ''
    pos = ""
    if args:
        places = int(args.split(',')[0].split('=')[1])
        dp = args.split(',')[1].split('=')[1]
        if len(args.split(',')) > 2:
            pos = args.split(',')[2].split('=')[1]
    else:
        places = 2
        dp = '.'
    return money_default_fmt(Decimal(value), places=places, dp=dp, pos=pos)


@register.filter
@stringfilter
def financial_frm(value, args=None):
    if not value or value == 'None':
        return ''
    pos = ""
    if args:
        places = int(args.split(',')[0].split('=')[1])
        dp = args.split(',')[1].split('=')[1]
        if len(args.split(',')) > 2:
            pos = args.split(',')[2].split('=')[1]
    else:
        places = 2
        dp = '.'

    value = Decimal(value)
    if value < 0:
        return "(%s)" % money_default_fmt(abs(Decimal(value)), places=places, dp=dp, pos=pos)
    else:
        return money_default_fmt(Decimal(value), places=places, dp=dp, pos=pos)


@register.filter
def datetime(value, arg=None):
    """Formats a date according to the given format."""
    from django.utils.dateformat import format
    if not value:
        return u''
    if arg is None:
        arg = settings.DATETIME_FORMAT
    try:
        return formats.date_format(value, arg)
    except AttributeError:
        try:
            return format(value, arg)
        except AttributeError:
            return ''


datetime.is_safe = False


def convert_sort(previous_sort, param_name):
    if previous_sort and previous_sort == param_name:
        return '-' + param_name
    return param_name


class GetParamsNode(template.Node):
    def __init__(self, param_name, param_value):
        self.param_name = param_name
        self.param_value = param_value

    def render(self, context):
        res = []
        for key, value in context['request'].GET.items():
            if key != self.param_name:
                res.append('%s=%s' % (key, value))
        res.append('%s=%s' % (self.param_name, convert_sort(context.get('prev_sort'), self.param_value)))
        return '?' + '&'.join(res)


@register.tag
def update_get_params(parser, token):
    try:
        tag_name, current_param_name, current_param_value = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a two arguments" % token.contents.split()[0])
    return GetParamsNode(current_param_name, current_param_value)


@register.filter
def round_over_four(value, args=None):
    if value is None:
        return None
    if value > 4:
        return int(value)
    return value


@register.filter
def decimal_to_time(value, args=None):
    """Formats a time from Decimal or int to HH:MM format."""
    if isinstance(value, Decimal):
        return "%d:%02d" % (int(value), int(value % 1 * 60))
    elif isinstance(value, int):
        return value
    return '0:00'


@register.filter(name='percent')
def percent(value, arg=None):
    if value in (None, ''):
        return None
    if arg is None:
        return 100
    if arg == 0:
        return 0
    return round(value / arg * 100, 2)


@register.filter(name='diagramm_percent')
def diagramm_percent(value, arg=None):
    if value in (None, ''):
        return None
    if arg is None:
        return 100
    if arg == 0:
        return 0
    try:
        return int(round(value * 1. / arg * 100 / 10) * 10)
    except ZeroDivisionError:
        return 0


numeric_test = re.compile("^\d+$")


@register.filter(name='getattribute')
def getattribute(value, arg):
    """
    Gets an attribute of an object dynamically from a string name
    """
    if hasattr(value, str(arg)):
        return getattr(value, arg)
    elif hasattr(value, '__getitem__') and hasattr(value, '__contains__') and arg in value:
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID


register.filter('getattribute', getattribute)


@register.filter(name='percent')
def percent(value, arg=None):
    if value in (None, ''):
        return None
    if arg is None:
        return 100
    if arg == 0:
        return 0
    try:
        return round(float(value) / float(arg) * 100, 2)
    except ZeroDivisionError:
        return None


@register.filter(name='divide')
def divide(value, arg):
    return value / arg


@register.filter(name='times')
def times(number):
    if isinstance(number, float):
        return range(int(round(number, 0)))


@register.filter(name='disabled_stars_times')
def disabled_stars_times(number):
    if isinstance(number, float):
        return range(int(round(5 - number, 0)))


@register.filter(name='paginator_slice')
def paginator_slice(value, page_range):
    page_range = int(page_range)
    return value.paginator.page_range[max(0, value.number - page_range): value.number + page_range]


@register.simple_tag(takes_context=True)
def cookie(context, cookie_name):  # could feed in additional argument to use as default value
    request = context['request']
    result = request.COOKIES.get(cookie_name, '')  # I use blank as default value
    return result


@register.simple_tag(takes_context=True)
def get_mobile_os(context):
    request = context['request']
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    ios = re.compile(r'iPad|iPod|iPhone', re.IGNORECASE)
    android = re.compile(r'Android', re.IGNORECASE)
    if re.search(ios, user_agent):
        return 'ios'
    elif re.search(android, user_agent):
        return 'android'
    else:
        return 'unknown'


@register.filter(name='get_class')
def get_class(value):
    return value.__class__.__name__


@register.simple_tag
def assign(value):
    return value


@register.filter(name='sort')
def sort(value):
    return sorted(list(value))


@register.filter(name='to_json')
def to_json(value):
    try:
        return json.loads(unquote(value))
    except ValueError:
        return {}


@register.filter(name='is_in')
def inlist(value, args):
    if args is None:
        return False
    _list = [arg.strip() for arg in args.split(',')]
    return value in _list


@register.filter
def to_digit(value):
    try:
        value = int(value)
    except ValueError:
        value = None
    return value


@register.filter(is_safe=True)
@stringfilter
def truncate_filename(value, arg):
    try:
        length = int(arg)
    except ValueError:
        return value
    name, ext = os.path.splitext(value)
    name = Truncator(name).chars(length, '... ')
    return '%s%s' % (name, ext)


@register.filter
def get_true_url(url):
    if url.startswith('http://www.'):
        return 'http://' + url[len('http://www.'):]
    if url.startswith('www.'):
        return 'http://' + url[len('www.'):]
    if not url.startswith('http://') and not url.startswith('https://'):
        return 'http://' + url
    return url


@register.filter
def split_list(data, n):
    n = int(n)
    return [data[x:x + n] for x in range(0, len(data), n)]


@register.filter
def get_language_name(language_code):
    for code, name in settings.LANGUAGES:
        if code == language_code:
            return name
    return language_code


@register.simple_tag(takes_context=True)
def get_invitation_redirect_url(context):
    request = context['request']
    if request.session.get('user_login'):
        return reverse('user-social-invitation-redirect', host='my')
    else:
        return request.build_absolute_uri()


from django.template.exceptions import TemplateSyntaxError

kwarg_re = re.compile(r"(?:(\w+)=)?(.+)")


class URLNode(Node):
    def __init__(self, view_name, args, kwargs, asvar):
        self.view_name = view_name
        self.args = args
        self.kwargs = kwargs
        self.asvar = asvar

    def render(self, context):
        from django.urls import reverse, NoReverseMatch
        args = [arg.resolve(context) for arg in self.args]
        kwargs = {k: v.resolve(context) for k, v in self.kwargs.items()}
        view_name = self.view_name.resolve(context)
        try:
            current_app = context.request.current_app
        except AttributeError:
            try:
                current_app = context.request.resolver_match.namespace
            except AttributeError:
                current_app = None
        # Try to look up the URL. If it fails, raise NoReverseMatch unless the
        # {% url ... as var %} construct is used, in which case return nothing.
        url = ''
        if args == [None]:
            view_name = "%s-root" % view_name
            args = []
        else:
            team_slug = kwargs.pop('team_slug', None)
            if team_slug:
                kwargs['team_slug'] = team_slug
            else:
                view_name = "%s-root" % view_name
                args = []
        try:
            url = reverse(view_name, args=args, kwargs=kwargs, current_app=current_app)
        except NoReverseMatch:
            if self.asvar is None:
                raise

        if self.asvar:
            context[self.asvar] = url
            return ''
        else:
            if context.autoescape:
                url = conditional_escape(url)
            return url


@register.tag
def branded_url(parser, token):
    r"""
    Return an absolute URL matching the given view with its parameters.

    This is a way to define links that aren't tied to a particular URL
    configuration::

        {% url "url_name" arg1 arg2 %}

        or

        {% url "url_name" name1=value1 name2=value2 %}

    The first argument is a URL pattern name. Other arguments are
    space-separated values that will be filled in place of positional and
    keyword arguments in the URL. Don't mix positional and keyword arguments.
    All arguments for the URL must be present.

    For example, if you have a view ``app_name.views.client_details`` taking
    the client's id and the corresponding line in a URLconf looks like this::

        path('client/<int:id>/', views.client_details, name='client-detail-view')

    and this app's URLconf is included into the project's URLconf under some
    path::

        path('clients/', include('app_name.urls'))

    then in a template you can create a link for a certain client like this::

        {% url "client-detail-view" client.id %}

    The URL will look like ``/clients/client/123/``.

    The first argument may also be the name of a template variable that will be
    evaluated to obtain the view name or the URL name, e.g.::

        {% with url_name="client-detail-view" %}
        {% url url_name client.id %}
        {% endwith %}
    """
    bits = token.split_contents()
    if len(bits) < 2:
        raise TemplateSyntaxError("'%s' takes at least one argument, a URL pattern name." % bits[0])
    viewname = parser.compile_filter(bits[1])
    args = []
    kwargs = {}
    asvar = None
    bits = bits[2:]

    if len(bits) >= 2 and bits[-2] == 'as':
        asvar = bits[-1]
        bits = bits[:-2]

    for bit in bits:
        match = kwarg_re.match(bit)
        if not match:
            raise TemplateSyntaxError("Malformed arguments to url tag")
        name, value = match.groups()
        if name:
            kwargs[name] = parser.compile_filter(value)
        else:
            args.append(parser.compile_filter(value))

    return URLNode(viewname, args, kwargs, asvar)


@register.simple_tag
def assign(value):
    return value


@register.simple_tag
def url_replace(request, field, value):
    if request.method == 'GET':
        _dict = request.GET.copy()
    else:
        request.method == 'POST'
        _dict = request.POST.copy()

    _dict[field] = value
    return _dict.urlencode()


@register.simple_tag
def url_delete(request, field):
    if request.method == 'GET':
        _dict = request.GET.copy()
    else:
        _dict = request.POST.copy()

    del _dict[field]
    return _dict.urlencode()


@register.simple_tag
def activate_current_timezone():
    current_timezone = settings.TIME_ZONE_DEFAULT
    timezone.activate(pytz.timezone(current_timezone))
    return current_timezone


@register.simple_tag
def url_replace_multiple(request, fields, values):
    if request.method == 'GET':
        _dict = request.GET.copy()
    else:
        request.method == 'POST'
        _dict = request.POST.copy()

    if len(fields) == len(values):
        for field, value in zip(fields, values):
            _dict[field] = value

    return _dict.urlencode()
