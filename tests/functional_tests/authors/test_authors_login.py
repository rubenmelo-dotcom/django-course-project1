import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .base import AuthorsBaseTest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_seccessfully(self):
        user_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=user_password, first_name='My_Name')

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.get_by_placeholder(
            form, 'Type your username').send_keys(user.username)
        self.get_by_placeholder(
            form, 'Type your password').send_keys(user_password)

        form.submit()

        self.assertIn(
            f'You are logged in with {user.first_name}',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_user_incorrect_data_can_login_seccessfully(self):
        user_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=user_password, first_name='My_Name')

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.get_by_placeholder(
            form, 'Type your username').send_keys(user.username)
        self.get_by_placeholder(
            form, 'Type your password').send_keys('pass_error')

        form.submit()

        self.assertIn(
            'Invalid credentials', self.browser.find_element(
                By.TAG_NAME, 'body'
            ).text
        )

    def test_user_invalid_data_can_login_seccessfully(self):
        user_password = 'pass'
        user = User.objects.create_user(
            username='my_user', password=user_password, first_name='My_Name')

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.get_by_placeholder(
            form, 'Type your username').send_keys(user.username)
        self.get_by_placeholder(
            form, 'Type your password').send_keys('')

        form.submit()

        self.assertIn(
            'Invalid username or password', self.browser.find_element(
                By.TAG_NAME, 'body'
            ).text
        )

    def test_login_create_raises_404_POST_method(self):
        self.browser.get(
            self.live_server_url +
            reverse('authors:login_create')
        )

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text)
