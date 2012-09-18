from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from forms import ClassroomForm
from models import Classroom, Edition


def classroom_add(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        context_data = {'form': form}

        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.leader = request.user.get_profile()
            classroom.save()

            redirect_url = reverse('classroom-view',
                    kwargs={'pk': classroom.id})

            return HttpResponseRedirect(redirect_url)
    else:
        form = ClassroomForm()
        context_data = {'form': form}

    return render_to_response('editions/classrooms/form.html', context_data,
            context_instance=RequestContext(request))


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


class ClassroomUpdate(UpdateView):
    model = Classroom
    form_class = ClassroomForm
    template_name = 'editions/classrooms/form.html'


class ClassroomListView(ListView):
    context_object_name = 'classrooms_list'
    template_name = 'editions/classrooms/index.html'

    def get_context_data(self, **kwargs):
        context = super(ClassroomListView, self).get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Classroom.objects.all()


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
