from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^backend/', include(admin.site.urls)),

        url(r'^accounts/',
            include('registration.backends.default.urls')),
        url(r'^comments/', include('django.contrib.comments.urls')),

        url(r'^edition/', include('editions.urls')),

        url(r'^grappelli/', include('grappelli.urls')),

        url(r'^tinymce/', include('tinymce.urls')),

        url('^about$', direct_to_template, {'template': 'about.html'},
            name='about'),
        url('^$', direct_to_template, {'template': 'index.html'},
            name='home'),
        )
