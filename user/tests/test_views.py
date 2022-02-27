from curses import reset_prog_mode
from urllib import response
from django.test import Client, TestCase
from django.urls import reverse
from user.models import User


class TestUserViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        testuser = User.objects.create(full_name="Test User", email="test@test.com")
        testuser.set_password("123")
        testuser.save()
        self.testuser = testuser

    def test_register_get(self):
        response = self.client.get(reverse("user:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")

    def test_register_post(self):
        response = self.client.post(
            reverse("user:register"),
            {
                "full_name": "Test User 2",
                "email": "test3@test.com",
                "password1": "Tuser123456",
                "password2": "Tuser123456",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:index"))

    def test_login_get(self):
        response = self.client.get(reverse("user:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_login_post(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "test@test.com",
                "password": "123",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:index"))

    def test_logout(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(reverse("user:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("travel:index"))

    def test_profile_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("user:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/profile.html")

    def test_edit_profile_get(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.get(reverse("user:edit_profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/edit_profile.html")

    def test_edit_profile_post(self):
        self.client.login(username="test@test.com", password="123")
        response = self.client.post(
            reverse("user:edit_profile"),
            {
                "full_name": "Test User 2",
                "email": "test3@test.com",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user:profile"))
