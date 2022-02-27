from django.test import TestCase
from user.models import User


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testuser = User.objects.create(full_name="Test User", email="test@test.com", password="123")
        cls.testuser2 = User.objects.create(
            full_name="Test User 2", email="test2@test.com", avatar="avatar.png", password="123"
        )

    def test_get_avatar(self):
        self.assertEqual(self.testuser2.get_avatar, "/media/avatar.png")

    def test_get_avatar_no_avatar(self):
        self.assertEqual(self.testuser.get_avatar, "/static/user/img/default.png")

    def test_avatar_preview(self):
        self.assertEqual(self.testuser2.avatar_preview, '<img src="/media/avatar.png" width="50" height="50" />')

    def test_avatar_preview_no_avatar(self):
        self.assertEqual(self.testuser.avatar_preview, "Not set")

    def test_instance_str(self):
        self.assertEqual(self.testuser.__repr__(), "[test@test.com]")

    def test_instance_repr(self):
        self.assertEqual(self.testuser.__str__(), "test@test.com")

    def test_has_perm(self):
        self.assertEqual(self.testuser.has_perm("test_perm"), True)

    def test_has_module_perm(self):
        self.assertEqual(self.testuser.has_module_perms("test_app"), True)
