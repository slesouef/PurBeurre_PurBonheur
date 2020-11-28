from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from accounts.models import MyUser


class UpdateUserTestCases(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        options.add_argument("--headless")
        cls.selenium = WebDriver(options=options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        self.user = MyUser.objects.create_user(
            username="testuser",
            email="test@email.com",
            password="test",
            first_name="test",
            last_name="test"
        )
        self.client.login(username="testuser", password="test")
        cookie = self.client.cookies["sessionid"].value
        self.selenium.get(self.live_server_url)
        self.selenium.add_cookie({"name": "sessionid", "value": cookie, "path": "/"})

    def tearDown(self):
        self.user.delete()

    def testUpdateUserAllMandatoryFields(self):
        """Test that the update page behaves as expected when all fields are updated at once"""
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/update"))
        self.assertTrue(self.selenium.find_element_by_id("update"))
        self.assertTrue(self.selenium.find_element_by_id("id_first_name"))
        self.assertTrue(self.selenium.find_element_by_id("id_last_name"))
        self.assertTrue(self.selenium.find_element_by_id("id_email"))
        self.assertTrue(self.selenium.find_element_by_id("id_avatar"))
        firstname = self.selenium.find_element_by_id("id_first_name")
        firstname.send_keys("newFirstName")
        lastname = self.selenium.find_element_by_id("id_last_name")
        lastname.send_keys("newLastName")
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("newEmail@test.com")
        self.selenium.find_element_by_class_name("btn").click()
        # assert user info is updated in database
        updateduser = MyUser.objects.get(id=self.user.id)
        self.assertEqual(updateduser.first_name, "newFirstName", "the user's first name was not updated")
        self.assertEqual(updateduser.last_name, "newLastName", "the user's last name was not updated")
        self.assertEqual(updateduser.email, "newEmail@test.com", "the user's email was not updated")
        # assert user is redirected to profile page
        self.assertTrue(self.selenium.find_element_by_id("about"))

    def testUpdateUserFirstName(self):
        """Test that the update page behaves as expected when only the first name is updated"""
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/update"))
        firstname = self.selenium.find_element_by_id("id_first_name")
        firstname.send_keys("newFirstName")
        self.selenium.find_element_by_class_name("btn").click()
        updateduser = MyUser.objects.get(id=self.user.id)
        self.assertEqual("newFirstName", updateduser.first_name, "the user's first name was not updated")

    def testUpdateUserLastName(self):
        """Test that the updated page behaves as expected when only the last name is updated"""
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/update"))
        lastname = self.selenium.find_element_by_id("id_last_name")
        lastname.send_keys("newLastName")
        self.selenium.find_element_by_class_name("btn").click()
        updateduser = MyUser.objects.get(id=self.user.id)
        self.assertEqual("newLastName", updateduser.last_name, "the user's last name was not updated")

    def testUpdateUserEmail(self):
        """Test that the update page behaves as expected when only the email is updated"""
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/update"))
        email = self.selenium.find_element_by_id("id_email")
        email.send_keys("newEmail@test.com")
        self.selenium.find_element_by_class_name("btn").click()
        updateduser = MyUser.objects.get(id=self.user.id)
        self.assertEqual("newEmail@test.com", updateduser.email, "the user's email was not updated")

    def testUpdateEmailInvalidNoAtSign(self):
        """Test that the update fails as expected when the email is invalid"""
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/update"))
        email = self.selenium.find_element_by_id("id_email")
        new_email = "thisIsAFailingEmailFormatTest.com"
        email.send_keys(new_email)
        self.selenium.find_element_by_class_name("btn").click()
        updateduser = MyUser.objects.get(id=self.user.id)
        self.assertEqual(self.user.email, updateduser.email, "the user's email was updated "
                                                             "when it should not have been")
        # assert user is still in update page
        self.selenium.find_element_by_id("update")

    def testUpdateEmailInvalidNoDomainName(self):
        """Test that the update fails as expected when the email is invalid"""
        self.selenium.get("%s%s" % (self.live_server_url, "/accounts/update"))
        email = self.selenium.find_element_by_id("id_email")
        new_email = "test@failed"
        email.send_keys(new_email)
        self.selenium.find_element_by_class_name("btn").click()
        updateduser = MyUser.objects.get(id=self.user.id)
        self.assertEqual(self.user.email, updateduser.email, "the user's email was updated " 
                                                             "when it should not have been")
        # assert user is still in update page
        self.selenium.find_element_by_id("update")
        error = self.selenium.find_element_by_class_name("form-text")
        self.assertEqual("Saisissez une adresse de courriel valide.", error.text, "error text is not displayed")
