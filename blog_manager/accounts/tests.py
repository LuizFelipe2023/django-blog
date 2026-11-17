from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages import get_messages

User = get_user_model()

class AuthFlashMessagesTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='existing@example.com',
            full_name='Existing User',
            phone='123456789',
            password='validpassword123'
        )
        self.client = Client()

    def test_login_message(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'existing@example.com',
                'password': 'validpassword123'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Welcome back' in str(m) for m in messages_list))

    def test_register_message(self):
        response = self.client.post(
            reverse('register'),
            {
                'full_name': 'New Registered User',
                'email': 'newuser@example.com',
                'phone': '999888777',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('Welcome to NewsBlog' in str(m) for m in messages_list))

    def test_logout_message(self):
        self.client.login(email='existing@example.com', password='validpassword123')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertTrue(any('logged out' in str(m) for m in messages_list))


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            full_name='Original Name',
            phone='111222333',
            password='password123'
        )
        self.client = Client()

    def test_profile_view_get(self):
        self.client.login(email='user@example.com', password='password123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Original Name')

    def test_profile_update_post(self):
        self.client.login(email='user@example.com', password='password123')
        # Tiny 1x1 GIF
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00'
            b'\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile('test_avatar.gif', small_gif, content_type='image/gif')

        response = self.client.post(
            reverse('profile'),
            {
                'full_name': 'Updated Name',
                'phone': '999888777',
                'bio': 'Award-winning journalist.',
                'avatar': uploaded,
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Updated Name')
        self.assertEqual(self.user.phone, '999888777')
        self.assertEqual(self.user.bio, 'Award-winning journalist.')
        self.assertTrue(bool(self.user.avatar))
        # Cleanup uploaded avatar file
        if self.user.avatar:
            self.user.avatar.delete(save=False)
