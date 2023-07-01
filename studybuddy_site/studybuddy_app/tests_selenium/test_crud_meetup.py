from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from django.contrib.auth.models import User
# https://docs.djangoproject.com/en/4.2/ref/contrib/staticfiles/#django.contrib.staticfiles.testing.StaticLiveServerTestCase
# https://docs.djangoproject.com/en/4.2/topics/testing/tools/#django.test.LiveServerTestCase

from django.utils import timezone
from django.urls import reverse
from studybuddy_app.models import Meetup
import datetime


def create_meetup(meetup_title, meetup_location="Room 11", days=2):
    start_time = timezone.now() + datetime.timedelta(days=days)
    end_time = start_time + datetime.timedelta(hours=2)
    return Meetup.objects.create(
        title=meetup_title,
        location=meetup_location,
        start_time=start_time,
        end_time=end_time)


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ["user.yaml"] #, "meetup.yaml"]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
    # https://www.selenium.dev/documentation/webdriver/elements/finders/

    def get_url(self, path_name, args):
        prefix = "studybuddy_app:"
        if not path_name.startswith(prefix):
            path_name = f"{prefix}{path_name}"
        return f"{self.live_server_url}{reverse(path_name, args=args)}"
    
    def get_path(self, path_name, args=(), assert_found=True):
        url = self.get_url(path_name, args)
        self.selenium.get(url)
        if assert_found:
            self.assert_found()
        return url
       
    def assert_found(self):
        body = self.selenium.find_element(By.TAG_NAME, "body")
        assert not body.text.startswith('Not Found')

    def test_create_meetup(self):
        meetup_title = "Meetup created from Selenium"
        self.get_path('studybuddy_app:meetup.new')
    
        meetup_title_field = self.selenium.find_element(By.NAME, "title")
        meetup_title_field.send_keys(meetup_title)
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        self.selenium.get(f"{self.live_server_url}/studybuddy/meetups")
        self.assert_found()
        body = self.selenium.find_element(By.TAG_NAME, "body")
        assert meetup_title in body.text

    def test_edit_meetup(self):
        meetup = create_meetup('new meetup', 5)
        self.get_path('studybuddy_app:meetup.edit', args=(meetup.pk,))
        meetup_title_new = meetup.title + " edited"
        meetup_title_field = self.selenium.find_element(By.NAME, "title")
        meetup_title_field.send_keys(meetup_title_new)
        self.selenium.find_element(By.XPATH, '//input[@type="submit"]').click()
        self.get_path('studybuddy_app:meetup.path_meetups_pk', args=(meetup.pk,))
        self.assert_found()
        body = self.selenium.find_element(By.TAG_NAME, "body")
        assert meetup_title_new in body.text

    def test_delete_meetup(self):
        meetup = create_meetup('meetup to delete', 5)
        self.get_path('studybuddy_app:meetup.path_meetups_pk', args=(meetup.pk,))
        body = self.selenium.find_element(By.TAG_NAME, "body")
        assert meetup.title in body.text
        delete = self.selenium.find_element(By.LINK_TEXT, 'Delete')
        delete.click()
        self.get_path('meetup.path_meetups')
        #self.selenium.get(f"{self.live_server_url}/studybuddy/meetups")
        body = self.selenium.find_element(By.TAG_NAME, "body")
        self.assert_found()
        assert meetup.title not in body.text


    # def test_login(self):
    #     self.selenium.get(f"{self.live_server_url}/login/")
    #     username_input = self.selenium.find_element(By.NAME, "username")
    #     username_input.send_keys("myuser")
    #     password_input = self.selenium.find_element(By.NAME, "password")
    #     password_input.send_keys("secret")
    #     self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()