from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse

from profiles.forms import SignupForm

from faker import Factory

# Create your tests here.
faker = Factory.create()

class TestSignUpForm(TestCase):

    def setUp(self):

        # Create some test users
        test_user = User.objects.create_user(
            username='test_user',
            password='123456')
        test_user.save()

    def test_existent_username(self):

        data = {
            'username': 'test_user',
            'password': '123456',
            'password_confirmation': '123456'
        }
        form = SignupForm(data=data)
        self.assertFalse(form.is_valid())

    def test_form_valid(self):

        data = {
            'username': 'a_test_username',
            'password': '123456',
            'password_confirmation': '123456',
            'first_name': faker.first_name(),
            'last_name': faker.last_name(),
            'email': faker.email()
        }
        form = SignupForm(data=data)
        self.assertTrue(form.is_valid())