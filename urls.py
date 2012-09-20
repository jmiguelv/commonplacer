from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^edition/', include('editions.urls')),

        url(r'^admin/', include(admin.site.urls)),

        url(r'^grappelli/', include('grappelli.urls')),

        url(r'^tinymce/', include('tinymce.urls')),

        url('^$', direct_to_template, {'template': 'index.html'}),
        )
