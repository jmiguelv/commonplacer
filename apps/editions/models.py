from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from taggit.managers import TaggableManager


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def __unicode__(self):
        return u'%s' % (self.user)

    def get_classrooms(self):
        """Returns all the classrooms the current user is associated with."""
        leader = self.get_leader_classrooms()
        participant = self.get_participant_classrooms()

        return leader | participant

    def get_leader_classrooms(self):
        """Returns all the classrooms the current user is leader of."""
        return self.leader_classrooms.all() | \
                self.other_leaders_classrooms.all()

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

    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'pk': self.pk})


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
    author = models.ForeignKey(UserProfile, editable=False,
            related_name='author_editions')
    title = models.CharField(max_length=256)
    classroom = models.ForeignKey(Classroom, blank=True, null=True,
            related_name='editions')
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

    def get_absolute_url(self):
        return reverse('edition-detail', kwargs={'pk': self.pk})

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
            mine = Edition.objects.filter(author=user.get_profile())
            queryset = Edition.objects.exclude(permission__name='private')
            queryset = mine | queryset

        return queryset

    def display_annotations(self, user):
        display = False

        if not user.is_anonymous():
            profile = user.get_profile()

            if profile == self.author:
                display = True
            elif self.classroom:
                if profile == self.classroom.leader or \
                   profile in self.classroom.other_leaders.all():
                    display = True

        return display
