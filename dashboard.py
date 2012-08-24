from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from grappelli.dashboard import modules, Dashboard
from grappelli.dashboard.utils import get_admin_site_name


class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for www.
    """

    def init_with_context(self, context):
        site_name = get_admin_site_name(context)

        # append an app list module for "Administration"
        self.children.append(modules.ModelList(
            _('Administration'),
            collapsible=False,
            column=1,
            models=['django.contrib.*'],
            ))

        # append an app list module for "Editions"
        self.children.append(modules.ModelList(
            _('Editions'),
            collapsible=False,
            column=1,
            #css_classes=['collapse open'],
            models=['editions.*'],
            ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            limit=15,
            collapsible=False,
            column=3,
            ))
