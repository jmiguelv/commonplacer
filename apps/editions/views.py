from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from forms import ClassroomForm, EditionForm
from models import Classroom, Edition


class ClassroomCreate(CreateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'editions/classrooms/form.html'

    def form_valid(self, form):
        form.instance.leader = self.request.user.get_profile()
        return super(ClassroomCreate, self).form_valid(form)


class ClassroomDelete(DeleteView):
    model = Classroom
    template_name = 'editions/classrooms/confirm_delete.html'
    success_url = reverse_lazy('classroom-list')

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        obj = super(ClassroomDelete, self).get_object()

        if len(obj.editions.all()) > 0:
            messages.warning(request,
                    'You can\'t delete classrooms that have editions.')
            response = HttpResponseRedirect(reverse('classroom-delete',
                kwargs={'pk': obj.id}))

        profile = request.user.get_profile()

        if profile == obj.leader or profile in obj.other_leaders.all():
            response = super(ClassroomDelete, self).dispatch(request, *args,
                    **kwargs)
        else:
            messages.error(request,
                    'You don\'t have permissions to delete this classroom.')
            response = HttpResponseRedirect(reverse('classroom-detail',
                kwargs={'pk': obj.id}))

        return response


class ClassroomUpdate(UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'editions/classrooms/form.html'

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        obj = super(ClassroomUpdate, self).get_object()
        profile = request.user.get_profile()

        if profile == obj.leader or profile in obj.other_leaders.all():
            response = super(ClassroomUpdate, self).dispatch(request, *args,
                    **kwargs)
        else:
            messages.error(request,
                    'You don\'t have permissions to change this classroom.')
            response = HttpResponseRedirect(reverse('classroom-detail',
                kwargs={'pk': obj.id}))

        return response


class ClassroomListView(ListView):
    context_object_name = 'classrooms_list'
    template_name = 'editions/classrooms/index.html'

    def get_context_data(self, **kwargs):
        context = super(ClassroomListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Classroom.objects.all()


class EditionCreate(CreateView):
    model = Edition
    form_class = EditionForm
    template_name = 'editions/form.html'

    def get_form(self, form_class):
        form = super(EditionCreate, self).get_form(form_class)
        profile = self.request.user.get_profile()
        form.fields['classroom'].queryset = profile.get_classrooms()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user.get_profile()
        return super(EditionCreate, self).form_valid(form)


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
