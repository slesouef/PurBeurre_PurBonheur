from django.test import TestCase

from accounts.models import MyUser


class UnauthenticatedAccountsViewsTestCases(TestCase):
    """Verify the behaviour of the accounts app views when a user is not authenticated"""

    def test_login_page(self):
        """Test that login page returns HTTP 200"""
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        """Test that signup page returns HTTP 200"""
        response = self.client.get('/accounts/signup/')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/signup.html')

    def test_profile_page_unauthenticated_user(self):
        """Test that profile page redirects unauthenticated users to login"""
        response = self.client.get('/accounts/profile/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/profile/')

    def test_favorites_page_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login page"""
        response = self.client.get('/accounts/favorites/')
        self.assertRedirects(response, '/accounts/login/?next=/accounts/favorites/')

    def test_save_favorite_unauthenticated_user(self):
        """Test that save favorites raises Permission Denied for unauthenticated users"""
        response = self.client.get('/accounts/favorites/new/')
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, template_name='403.html')


class AuthenticatedAccountsViewsTestCases(TestCase):
    """Verify the behaviour of the accounts app views when the user is authenticated"""

    def setUp(self):
        """Create authenticated user"""
        self.user = MyUser.objects.create_user(username='test')
        self.client.force_login(self.user)

    def test_signup_authenticated_user(self):
        """Test that user is redirected to the profile page if authenticated"""
        response = self.client.get('/accounts/signup/')
        self.assertRedirects(response, '/accounts/profile/')

    def test_profile_page_authenticated_user(self):
        """Test that profile page is displayed for authenticated users"""
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/profile.html')

    def test_favorites_page_authenticated_user(self):
        """Test that favorites page is displayed for authenticated users"""
        response = self.client.get('/accounts/favorites/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/favorites.html')

    def test_logout(self):
        """Test that the logout link redirects ton index page"""
        response = self.client.get('/logout/')
        self.assertRedirects(response, '/')
