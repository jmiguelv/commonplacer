from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from models import Classroom, Edition, Permission, Status, \
        UserProfile
from tinymce.widgets import TinyMCE


class ClassroomAdmin(admin.ModelAdmin):
    model = Classroom

    filter_horizontal = ['other_leaders', 'participants']
    list_display = ['name', 'leader', 'created', 'modified']
    list_display_links = ['name', 'leader', 'created', 'modified']


class EditionAdmin(admin.ModelAdmin):
    model = Edition

    list_display = ['author', 'title', 'status', 'permission', 'created',
            'modified']
    list_display_links = ['author', 'title', 'status', 'permission', 'created',
            'modified']
    list_filter = ['status', 'permission']
    search_fields = ['title', 'text', 'comments']

    class Media:
        js = [settings.TINYMCE_JS_URL]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'text':
            return forms.CharField(widget=TinyMCE())
        return super(EditionAdmin, self).formfield_for_dbfield(db_field,
                **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'classroom':
            user = request.user.get_profile()
            kwargs['queryset'] = Classroom.objects.filter(participants=user)

        return super(EditionAdmin, self).formfield_for_foreignkey(db_field,
                request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.get_profile()
            obj.save()
        else:
            if request.user.get_profile() == obj.author:
                obj.save()
            else:
                message = 'You can only change Edition\'s you authored.'
                request.user.message_set.create(message=message)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.author = request.user.get_profile()
            instance.save()
        formset.save_m2m()


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['action_time', 'user', 'content_type', 'change_message',
            'is_addition', 'is_change', 'is_deletion']
    list_filter = ['action_time', 'user', 'content_type']
    ordering = ['-action_time']
    readonly_fields = ['user', 'content_type', 'object_id', 'object_repr',
            'action_flag', 'change_message']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # Returning False causes table to not show up in admin page
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class PermissionAdmin(admin.ModelAdmin):
    model = Permission

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


class StatusAdmin(admin.ModelAdmin):
    model = Status

    list_display = ['name', 'created', 'modified']
    list_display_links = ['name', 'created', 'modified']
    search_fields = ['name']


admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Edition, EditionAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(UserProfile)
