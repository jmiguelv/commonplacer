from django.conf import settings
from django.contrib.auth.models import User, Group
from django.test import TestCase
from models import Classroom


class UserProfileTest(TestCase):

    def setUp(self):
        moderators = \
                Group.objects.create(name=settings.EDITIONS_GROUP_MODERATORS)
        leaders = \
                Group.objects.create(name=settings.EDITIONS_GROUP_LEADERS)
        participants = \
                Group.objects.create(name=settings.EDITIONS_GROUP_PARTICIPANTS)

        self.moderator = User.objects.create_user('moderator',
                'moderator@commonplacer.org',
                None).get_profile()
        self.leader = User.objects.create_user('leader',
                'leader@commonplacer.org',
                None).get_profile()
        self.participant = User.objects.create_user('participant',
                'participant@commonplacer.org',
                None).get_profile()

        moderators.user_set.add(self.moderator.user)
        leaders.user_set.add(self.leader.user)
        participants.user_set.add(self.participant.user)

        self.classroom = Classroom(name='TestClassroom', leader=self.leader)
        self.classroom.save()
        self.classroom.participants.add(self.participant)

    def test_get_leader_classrooms(self):
        """Tests getting a leader's classrooms"""
        self.assertEqual(self.classroom, self.leader.get_leader_classrooms()[0])
        self.assertEqual(0, self.participant.get_leader_classrooms().count())

    def test_get_participant_classrooms(self):
        """Tests getting a participant's classrooms"""
        self.assertEqual(self.classroom,
                self.participant.get_participant_classrooms()[0])
        self.assertEqual(0, self.leader.get_participant_classrooms().count())

    def test_is_moderator(self):
        """Tests if the given user is in the moderators group"""
        self.assertTrue(self.moderator.is_moderator())
        self.assertFalse(self.leader.is_moderator())
        self.assertFalse(self.participant.is_moderator())

    def test_is_leader(self):
        """Tests if the given user is in the leaders group"""
        self.assertFalse(self.moderator.is_leader())
        self.assertTrue(self.leader.is_leader())
        self.assertFalse(self.participant.is_leader())

    def test_is_participant(self):
        """Tests if the given user is in the participant group"""
        self.assertFalse(self.moderator.is_participant())
        self.assertFalse(self.leader.is_participant())
        self.assertTrue(self.participant.is_participant())
