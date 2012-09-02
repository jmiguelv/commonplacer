from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from forms import ClassroomForm
from models import Classroom, Edition


class ClassroomListView(ListView):
    context_object_name = 'classrooms_list'
    template_name = 'editions/classrooms/index.html'

    def get_context_data(self, **kwargs):
        context = super(ClassroomListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Classroom.objects.all()


class ClassroomUpdateView(UpdateView):
    model = Classroom
    template_name = 'editions/classrooms/form.html'


class TagEditionListView(ListView):
    context_object_name = 'editions_list'
    template_name = 'editions/index.html'

    def get_context_data(self, **kwargs):
        context = super(TagEditionListView, self).get_context_data(**kwargs)
        context['facet'] = 'tag'
        context['facet_value'] = self.args[0]
        return context

    def get_queryset(self):
        qs = Edition.get_queryset(self.request.user)
        return qs.filter(tags__name__in=[self.args[0]]).order_by('-modified')


class EditionListView(ListView):
    context_object_name = 'editions_list'
    template_name = 'editions/index.html'

    def get_context_data(self, **kwargs):
        context = super(EditionListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Edition.get_queryset(self.request.user).order_by('-modified')


class AuthorEditionListView(ListView):
    context_object_name = 'editions_list'
    template_name = 'editions/index.html'

    def get_context_data(self, **kwargs):
        context = super(AuthorEditionListView, self).get_context_data(**kwargs)
        context['facet'] = 'author'
        context['facet_value'] = self.args[0]
        return context

    def get_queryset(self):
        author = get_object_or_404(User, username=self.args[0])
        qs = Edition.get_queryset(self.request.user)
        return qs.filter(author=author).order_by('-modified')
