try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('sentry-opsgenie').version
except Exception, e:
    VERSION = 'unknown'
