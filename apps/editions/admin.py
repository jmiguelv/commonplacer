from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group
from models import Classroom, Edition, Feedback, Permission, Status, \
        UserProfile
from tinymce.widgets import TinyMCE


class ClassroomAdmin(admin.ModelAdmin):
    model = Classroom

    filter_horizontal = ['participants']
    list_display = ['name', 'leader', 'created', 'modified']
    list_display_links = ['name', 'leader', 'created', 'modified']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'leader':
            group = Group.objects.get(name=settings.EDITIONS_GROUP_LEADERS)
            user_set = group.user_set.all()
            kwargs['queryset'] = UserProfile.objects.filter(user__in=user_set)

        return super(ClassroomAdmin,
                self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        participants = settings.EDITIONS_GROUP_PARTICIPANTS

        if db_field.name == participants:
            group = Group.objects.get(name=participants)
            user_set = group.user_set.all()
            kwargs['queryset'] = UserProfile.objects.filter(user__in=user_set)

        return super(ClassroomAdmin,
                self).formfield_for_manytomany(db_field, request, **kwargs)


class FeedbackInline(admin.StackedInline):
    model = Feedback

    classes = ('collapse open',)
    extra = 0
    inline_classes = ('collapse open',)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class EditionAdmin(admin.ModelAdmin):
    model = Edition

    inlines = [FeedbackInline]
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

    def queryset(self, request):
        return Edition.get_admin_queryset(request.user)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
            obj.save()
        else:
            if request.user == obj.author:
                obj.save()
            else:
                message = 'You can only change Edition\'s you authored.'
                request.user.message_set.create(message=message)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            instance.author = request.user
            instance.save()
        formset.save_m2m()


class FeedbackAdmin(admin.ModelAdmin):
    model = Feedback

    list_display = ['author', 'edition', 'created', 'modified']
    list_display_links = ['author', 'edition', 'created', 'modified']
    search_fields = ['text']


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
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(UserProfile)
