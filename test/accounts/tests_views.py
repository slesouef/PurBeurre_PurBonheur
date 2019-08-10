from django.test import TestCase, Client

from accounts.models import MyUser


class PageViewsTestCase(TestCase):

    def test_login_page(self):
        """Test that login page returns HTTP 200"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        """Test that signup page returns HTTP 200"""
        response =self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)

    def test_signup_authenticated_user(self):
        """Test that user is reditrected to the profile page if authenticated"""
        c = Client()
        c.force_login(MyUser.objects.get_or_create(username='test')[0])
        response = c.get('/accounts/signup/')
        self.assertRedirects(response, '/accounts/profile/')

    def test_profile_page_unauthenticated_user(self):
        """Test that profile page redirects unauthenticated users to login"""
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, '/accounts/login/?next=%2Faccounts%2Fprofile%2F')

    def test_profile_page_authenticated_user(self):
        """Test that profile page is displayed for authenticated users"""
        c = Client()
        c.force_login(MyUser.objects.get_or_create(username='test')[0])
        response = c.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_favorites_page_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login page"""
        response = self.client.get('/accounts/favorites/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/favorites/')

    def test_favorites_page_authenticated_user(self):
        """Test that favorites page is displayed for authenticated users"""
        c = Client()
        c.force_login(MyUser.objects.get_or_create(username='test')[0])
        response = c.get('/accounts/favorites/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        """Test that the logout link redirects ton index page"""
        c = Client()
        c.force_login(MyUser.objects.get_or_create(username='test')[0])
        response = c.get('/logout/')
        self.assertRedirects(response, '/')
