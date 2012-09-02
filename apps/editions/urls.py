from django.conf.urls.defaults import patterns, url
from django.views.generic import DetailView
from models import Classroom, Edition
from views import AuthorEditionListView, ClassroomListView, EditionListView, \
        TagEditionListView

urlpatterns = patterns('',
        url(r'^$', EditionListView.as_view()),
        url(r'^(?P<pk>\d+)/$',
            DetailView.as_view(
                model=Edition,
                template_name='editions/detail.html')),
            url(r'^tag/(\w+)/$', TagEditionListView.as_view()),
            url(r'^author/(\w+)/$', AuthorEditionListView.as_view()),
            url(r'^classrooms/$', ClassroomListView.as_view()),
            url(r'^classrooms/(?P<pk>\d+)/$', DetailView.as_view(
                model=Classroom,
                template_name='editions/classrooms/detail.html')),
            )
