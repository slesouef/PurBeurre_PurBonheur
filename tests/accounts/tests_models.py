from django.test import TestCase

from accounts.models import MyUser, user_directory_path


class UserFileUploadPathTestCase(TestCase):
    """Verify that the file upload path method returns the correct path
     values"""

    def test_upload_path(self):
        """The user's avatar file is uploaded in a user specific directory of
        the user's username"""
        user = MyUser(username='test')
        path = user_directory_path(user, 'test_file.txt')
        self.assertIn('test', path)
        self.assertIn('test_file.txt', path)
