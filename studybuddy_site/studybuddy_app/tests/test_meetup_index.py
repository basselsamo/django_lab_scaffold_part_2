import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from studybuddy_app.models import Meetup


def create_meetup(meetup_title, meetup_location="Room 11", days=2):
    start_time = timezone.now() + datetime.timedelta(days=days)
    end_time = start_time + datetime.timedelta(hours=2)
    return Meetup.objects.create(
        title=meetup_title,
        location=meetup_location,
        start_time=start_time,
        end_time=end_time)


class MeetupIndexViewTests(TestCase):
    def test_no_meetups(self):
        response = self.client.get(
            reverse("studybuddy_app:meetup.path_meetups"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No Meetups are available.")
        self.assertQuerySetEqual(response.context["meetup_list"], [])

    def test_meetup_list(self):
        meetup = create_meetup(meetup_title="a meetup title", days=3)
        response = self.client.get(
            reverse("studybuddy_app:meetup.path_meetups"))
        self.assertQuerySetEqual(
            response.context["meetup_list"],
            [meetup],
        )

    def test_past_meetups_are_not_shown(self):
        _meetup = create_meetup(meetup_title="a meetup title", days=-2)
        response = self.client.get(
            reverse("studybuddy_app:meetup.path_meetups"))
        self.assertContains(response, "No Meetups are available.")
        self.assertQuerySetEqual(
            response.context["meetup_list"], [])

    def test_future_meetup_and_past_meetup(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        meetup = create_meetup(meetup_title="Past meetup", days=-2)
        meetup_upcoming = create_meetup(meetup_title="Future meetup", days=2)
        response = self.client.get(
            reverse("studybuddy_app:meetup.path_meetups"))
        self.assertQuerySetEqual(
            response.context["meetup_list"], [meetup_upcoming])

    def test_two_future_meetups(self):
        meetup_1 = create_meetup(meetup_title="Future meetup 1", days=2)
        meetup_2 = create_meetup(meetup_title="Future meetup 2", days=3)
        response = self.client.get(
            reverse("studybuddy_app:meetup.path_meetups"))
        self.assertQuerySetEqual(
            response.context["meetup_list"], [meetup_1, meetup_2])
        