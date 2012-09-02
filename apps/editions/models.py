from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'%s' % (self.user)

    def get_leader_classrooms(self):
        """Returns all the classrooms the current user is leader of."""
        return self.leader_classrooms.all()

    def get_participant_classrooms(self):
        """Returns all the classrooms the current user is participant in."""
        return self.participant_classrooms.all()

    def is_moderator(self):
        """Returns True if the current user is part of the moderators
        groups, False otherwise."""
        group_name = settings.EDITIONS_GROUP_MODERATORS

        return self.is_in_group(group_name)

    def is_in_group(self, group_name):
        """Returns True if the current user is part of the given group."""
        return self.user.groups.filter(name=group_name).count() == 1

    def is_leader(self):
        """Returns True if the current user is part of the leaders groups,
        False otherwise."""
        group_name = settings.EDITIONS_GROUP_LEADERS

        return self.is_in_group(group_name)

    def is_participant(self):
        """Returns True if the current user is part of the participants groups,
        False otherwise."""
        group_name = settings.EDITIONS_GROUP_PARTICIPANTS

        return self.is_in_group(group_name)


# http://djangosnippets.org/snippets/500/
def user_post_save(sender, instance, **kwargs):
    """Makes the ORM create a profile each time an user is created (or updated,
    if the user profile lost), including 'admin' user."""
    UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(user_post_save, sender=User)


class Classroom(models.Model):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField()
    leader = models.ForeignKey(UserProfile, related_name="leader_classrooms")
    other_leaders = models.ManyToManyField(UserProfile, blank=True, null=True,
            related_name='other_leaders_classrooms')
    participants = models.ManyToManyField(UserProfile, blank=True, null=True,
            related_name='participant_classrooms')
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.leader)


class Permission(models.Model):
    name = models.CharField(max_length=32)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)


class Status(models.Model):
    name = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Status'

    def __unicode__(self):
        return u'%s' % (self.name)


class Edition(models.Model):
    author = models.ForeignKey(User, editable=False)
    title = models.CharField(max_length=256)
    classroom = models.ForeignKey(Classroom, blank=True, null=True)
    status = models.ForeignKey(Status)
    permission = models.ForeignKey(Permission)
    text = models.TextField()
    comments = models.TextField(blank=True, null=True)
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return u'%s' % (self.title)

    @staticmethod
    def get_admin_queryset(user):
        """Returns a queryset to be used in the admin interface. The objects in
        the queryset depend on the group the user belongs to. Site admins and
        moderators can view all the editions; leaders can view all the editions
        from the students in their classrooms; and participants can only view
        their own editions."""
        queryset = Edition.objects
        profile = user.get_profile()

        if user.is_superuser or profile.is_moderator():
            queryset = queryset.all()
        elif profile.is_leader():
            classrooms = profile.get_leader_classrooms()
            participant_set = set()

            for classroom in classrooms:
                for participant in classroom.participants.all():
                    participant_set.add(participant)

            queryset = queryset.filter(author__in=participant_set)
        elif profile.is_participant():
            queryset = queryset.filter(author=user)

        return queryset

    @staticmethod
    def get_queryset(user):
        """Returns a queryset to be used in the public part of the site. If the
        user is anonymous (non-authenticated) it can only view public editions.
        Otherwise, it can view it's own editions plus all non-private
        editions."""
        queryset = None

        if user.is_anonymous():
            queryset = Edition.objects.filter(permission__name='public')
        else:
            queryset = Edition.get_admin_queryset(user)
            queryset = queryset | \
                    Edition.objects.exclude(permission__name='private')

        return queryset


class Feedback(models.Model):
    edition = models.ForeignKey(Edition)
    author = models.ForeignKey(User, editable=False)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, auto_now_add=True,
            editable=False)

    class Meta:
        verbose_name_plural = 'Feedback'

    def __unicode__(self):
        return u'%s. %s' % (self.author, self.edition)
