from authors.forms import RegisterForm
from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('username', 'Your username'),
        ('email', 'Your e-mail'),
        ('password', 'Your password'),
        ('password2', 'Repeat your password here')
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, current_placeholder)

    @parameterized.expand([
        ('username', 'Username must be have letters, numbers or one of those @/./+/-/_. ' \
            'The length should be between 4 and 150 characters.'),
        ('email', 'The e-mail must be valid'),
        ('password', 'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(needed, current)

    @parameterized.expand([
        ('first_name', 'First name'),
        ('last_name', 'Last name'),
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('password', 'Password'),
        ('password2', 'Password2')
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(needed, current)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'first_name': 'First',
            'last_name': 'Last',
            'username': 'User',
            'email': 'email@anyemail.com',
            'password': 'Str0ngP@ssword1',
            'password2': 'Str0ngP@ssword1',
        }
        return super().setUp(*args, **kwargs)
    
    @parameterized.expand([
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('username', 'This field must not be empty'),
        ('email', 'The e-mail must be valid'),
        ('password', 'Password must not be empty'),
        ('password2', 'Repeat your password here'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have at least 4 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Username must have a maximum 150 characters'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'abcd1234'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        )

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        
        self.form_data['password'] = 'ABcd1234'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data['password'] = 'ABcd1234'
        self.form_data['password2'] = 'ABcd12345'
        
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'Password and password2 must be equal'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.context['form'].errors.get('password2'))
        
        self.form_data['password'] = 'ABcd1234'
        self.form_data['password2'] = 'ABcd1234'
        
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_send_get_request_to_registration_view_returns_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    # def test_email_field_must_be_unique(self):
    #     url = reverse('authors:register_create')

    #     self.client.post(url, data=self.form_data, follow=True)
    #     self.form_data['firstname'] = 'OtherFirst'
    #     self.form_data['lastname'] = 'OtherLast'
    #     self.form_data['username'] = 'OtherUser'
    #     response = self.client.post(url, data=self.form_data, follow=True)

    #     msg = 'User e-mail is already in use'
    #     email_errors = response.context['form'].errors.get('email', [])
    #     self.assertIn(msg, email_errors)
    #     self.assertIn(msg, response.content.decode('utf-8'))
    
    def test_author_created_can_login(self):
        url = reverse('authors:register_create')

        self.form_data.update({
            'username': 'testuser',
            'password': 'ABcd1234',
            'password2': 'ABcd1234',
        })

        self.client.post(url, data=self.form_data, follow=True)

        is_authenticated = self.client.login(
            username='testuser',
            password='ABcd1234'
        )

        self.assertTrue(is_authenticated)