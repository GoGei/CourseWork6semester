from django_hosts import patterns, host

host_patterns = patterns(
    '',
    host(r'', 'Public.urls', name='public'),
    host(r'manager', 'Manager.urls', name='manager'),
    # host(r'api', 'Api.urls', name='api'),
)
