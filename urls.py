from django.conf import settings
from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^editions/', include('editions.urls')),

        url(r'^admin/', include(admin.site.urls)),

        # serve static files
        (r'^media(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        (r'^static(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),

        url(r'^grappelli/', include('grappelli.urls')),

        url(r'^tinymce/', include('tinymce.urls')),
        )
