from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from models import Classroom, Edition
from views import AuthorEditionListView, \
        ClassroomCreate, ClassroomDelete, ClassroomListView, ClassroomUpdate, \
        EditionListView, \
        TagEditionListView

urlpatterns = patterns('editions.views',
        url(r'^$', EditionListView.as_view()),
        url(r'^(?P<pk>\d+)/$', DetailView.as_view(model=Edition,
            template_name='editions/detail.html')),
        url(r'^tag/(\w+)/$', TagEditionListView.as_view()),
        url(r'^author/(\w+)/$', AuthorEditionListView.as_view()),

        url(r'^classroom/$', ClassroomListView.as_view(),
            name='classroom-list'),
        url(r'^classroom/(?P<pk>\d+)/$',
            login_required(DetailView.as_view(model=Classroom,
                template_name='editions/classrooms/detail.html')),
            name='classroom-detail'),
        url(r'^classroom/add/$',
            login_required(ClassroomCreate.as_view()),
            name='classroom-add'),
        url(r'^classroom/(?P<pk>\d+)/delete/$',
            login_required(ClassroomDelete.as_view()),
            name='classroom-delete'),
        url(r'^classroom/(?P<pk>\d+)/edit/$',
            login_required(ClassroomUpdate.as_view()),
            name='classroom-update'),
        )
