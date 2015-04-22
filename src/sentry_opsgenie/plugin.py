"""
sentry_opsgenie.plugin
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2015 by Sentry Team, see AUTHORS for more details.
:license: Apache 2.0, see LICENSE for more details.
"""
import logging
import sentry_opsgenie

from django import forms
from django.utils.html import escape

from sentry import http
from sentry.plugins.bases import notify
from sentry.utils import json


class OpsGenieptionsForm(notify.NotificationConfigurationForm):
    api_key = forms.CharField(
        max_length=255,
        help_text='OpsGenie API key used for authenticating API requests',
        required=True,
    )
    recipients = forms.CharField(
        max_length=255,
        help_text='The user names of individual users or groups (comma seperated)',
        required=False,
    )
    alert_url = forms.CharField(
        max_length=255,
        label='OpsGenie Alert URL',
        widget=forms.TextInput(attrs={'class': 'span6', 'placeholder': 'e.g. https://api.opsgenie.com/v1/json/alert'}),
        help_text='It must be visible to the Sentry server',
        required=True,
    )


class OpsGeniePlugin(notify.NotificationPlugin):
    author = 'Sentry Team'
    author_url = 'https://github.com/getsentry'
    resource_links = (
        ('Bug Tracker', 'https://github.com/getsentry/sentry-opsgenie/issues'),
        ('Source', 'https://github.com/getsentry/sentry-opsgenie'),
    )

    title = 'OpsGenie'
    slug = 'opsgenie'
    description = 'Create OpsGenie alerts out of notifications.'
    conf_key = 'opsgenie'
    version = sentry_opsgenie.VERSION
    project_conf_form = OpsGenieptionsForm

    logger = logging.getLogger('sentry.plugins.opsgenie')

    def is_configured(self, project):
        return all((
            self.get_option(k, project)
            for k in ('api_key', 'alert_url')
        ))

    def get_form_initial(self, project=None):
        return {
            'alert_url': 'https://api.opsgenie.com/v1/json/alert',
        }

    # TODO(dcramer): this is duplicated from sentry-webhooks
    def get_group_data(self, group, event):
        data = {
            'id': str(group.id),
            'checksum': group.checksum,
            'project': group.project.slug,
            'project_name': group.project.name,
            'logger': group.logger,
            'level': group.get_level_display(),
            'culprit': group.culprit,
            'message': event.message,
            'url': group.get_absolute_url(),
        }
        data['event'] = dict(event.data or {})
        data['event']['tags'] = event.get_tags()
        return data

    def notify_users(self, group, event, fail_silently=False):
        if not self.is_configured(group.project):
            return

        api_key = self.get_option('api_key', group.project)
        recipients = self.get_option('recipients', group.project)
        alert_url = self.get_option('alert_url', group.project)

        message = getattr(group, 'message_short', group.message).encode('utf-8')

        payload = {
           'apiKey': api_key,
           'message': message,
           'source': 'Sentry',
           'details': self.get_group_data(group, event)
        }

        if recipients:
            payload['recipients'] = recipients

        req = http.safe_urlopen(alert_url, json=payload)
        resp = req.json()

        if resp.get('status') != 'successful':
            raise Exception('Unsuccessful response from OpsGenie: %s' % resp)
