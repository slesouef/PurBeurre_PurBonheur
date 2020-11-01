from django.test import TestCase
from django.contrib import auth
from io import BytesIO
from PIL import Image

from accounts.models import MyUser
from search.models import Products, Categories


def create_test_image():
    file = BytesIO()
    image = Image.new("RGBA", size=(50, 50), color=(155, 0, 0))
    image.save(file, "png")
    file.name = "test.png"
    file.seek(0)
    return file


class UnauthenticatedAccountsViewsTestCases(TestCase):
    """
    Verify the behaviour of the accounts app views when a user is not
    authenticated
    """

    def test_login_page(self):
        """Test that login page returns HTTP 200"""
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "registration/login.html")

    def test_signup_page(self):
        """Test that signup page returns HTTP 200"""
        response = self.client.get("/accounts/signup/")
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "accounts/signup.html")

    def test_signup_mandatory_fields(self):
        """Test the signup process"""
        form_data = {"username": "test",
                     "first_name": "test",
                     "last_name": "test",
                     "email": "test@test.com",
                     "password": "test"}
        response = self.client.post("/accounts/signup/", form_data)
        user = auth.get_user(self.client)
        new_entry = MyUser.objects.filter(username="test")
        self.assertTrue(len(new_entry) == 1)
        self.assertEqual(new_entry[0].get_full_name(), "test test")
        self.assertEqual(new_entry[0].email, "test@test.com")
        self.assertFalse(new_entry[0].avatar)
        self.assertRedirects(response, "/accounts/profile/")
        self.assertTrue(user.is_authenticated)

    def test_signup_optional_fields(self):
        """Test the signup process with an image"""
        form_data = {"username": "test",
                     "first_name": "test",
                     "last_name": "test",
                     "email": "test@test.com",
                     "password": "test",
                     "avatar": create_test_image()}
        response = self.client.post("/accounts/signup/", form_data)
        user = auth.get_user(self.client)
        new_entry = MyUser.objects.filter(username="test")
        self.assertTrue(len(new_entry) == 1)
        self.assertEqual(new_entry[0].get_full_name(), "test test")
        self.assertEqual(new_entry[0].email, "test@test.com")
        self.assertTrue(new_entry[0].avatar)
        self.assertRedirects(response, "/accounts/profile/")
        self.assertTrue(user.is_authenticated)

    def test_profile_page_unauthenticated_user(self):
        """Test that profile page redirects unauthenticated users to login"""
        response = self.client.get("/accounts/profile/")
        self.assertRedirects(response,
                             "/accounts/login/?next=/accounts/profile/")

    def test_favorites_page_unauthenticated_user(self):
        """Test that unauthenticated users are redirected to login page"""
        response = self.client.get("/accounts/favorites/")
        self.assertRedirects(response,
                             "/accounts/login/?next=/accounts/favorites/")

    def test_save_favorite_unauthenticated_user(self):
        """
        Test that save favorites raises Permission Denied for
        unauthenticated users
        """
        response = self.client.get("/accounts/favorites/new/")
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    def test_update_page_unauthenticated_user(self):
        """Test that the update page redirects unauthenticated users to login"""
        response = self.client.get("/accounts/update/")
        self.assertRedirects(response,
                             "/accounts/login/?next=/accounts/update/")


class AuthenticatedAccountsViewsTestCases(TestCase):
    """
    Verify the behaviour of the accounts app views when the user
    is authenticated
    """

    def setUp(self):
        """Create authenticated user"""
        self.user = MyUser.objects.create_user(username="test")
        self.client.force_login(self.user)

    def test_signup_authenticated_user(self):
        """Test that user is redirected to the profile page if authenticated"""
        response = self.client.get("/accounts/signup/")
        self.assertRedirects(response, "/accounts/profile/")

    def test_profile_page_authenticated_user(self):
        """Test that profile page is displayed for authenticated users"""
        response = self.client.get("/accounts/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_favorites_page_authenticated_user(self):
        """Test that favorites page is displayed for authenticated users"""
        response = self.client.get("/accounts/favorites/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "accounts/favorites.html")

    def test_update_page_authenticated_user(self):
        """Test that update page is displayed for authenticated users"""
        response = self.client.get("/accounts/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "search/base.html")
        self.assertTemplateUsed(response, "search/search_form.html")
        self.assertTemplateUsed(response, "accounts/update.html")

    def test_save_favorite_new(self):
        """
        Test that a new favorite is added for the user when called by an
        authenticated user and it is not already a favorite
        """
        cat = Categories.objects.create(name="name")
        prod = Products.objects.create(category=cat, name="name")
        prod_id = prod.id
        response = self.client.post("/accounts/favorites/new/",
                                    {"product_id": prod_id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"response": "OK"})
        favs = self.user.favorites.all()
        self.assertEqual(len(favs), 1)

    def test_save_favorite_already_exists(self):
        """
        Test that no new favorite is added for the user when called by an
        authenticated user and the favorite already exists
        """
        cat = Categories.objects.create(name="name")
        prod = Products.objects.create(category=cat, name="name")
        prod_id = prod.id
        self.user.favorites.add(prod)
        response = self.client.post("/accounts/favorites/new/",
                                    {"product_id": prod_id})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content,
                             {"error": "favorite already exists"})
        favs = self.user.favorites.all()
        self.assertEqual(len(favs), 1)

    def test_logout(self):
        """Test that the logout link redirects ton index page"""
        response = self.client.get("/logout/")
        self.assertRedirects(response, "/")

    def test_update_user_information(self):
        """Test that the user information can be updated with the update page"""
        form_data = {"first_name": "test2",
                     "last_name": "test2",
                     "email": "test@email.com",
                     "avatar": create_test_image()}
        original_entry = MyUser.objects.filter(username="test")
        original_avatar = original_entry[0].avatar
        response = self.client.post("/accounts/update/", form_data)
        updated_entry = MyUser.objects.filter(username="test")
        self.assertTrue(len(updated_entry) == 1)
        self.assertEqual(updated_entry[0].get_full_name(), "test2 test2")
        self.assertEqual(updated_entry[0].email, "test@email.com")
        self.assertTrue(updated_entry[0].avatar != original_avatar)
        self.assertRedirects(response, "/accounts/profile/")
