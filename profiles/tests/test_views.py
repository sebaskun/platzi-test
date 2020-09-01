from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from profiles.forms import SignupForm

from faker import Factory

# Create your tests here.
faker = Factory.create()

class TestProfilesViews(TestCase):

    def setUp(self):
        pass

    def test_render_correct_template_sign_up(self):
        pass

    def test_redirect_after_signup(self):
        pass
    
    def test_logout(self):
        pass

    def test_signup_fail(self):
        pass
