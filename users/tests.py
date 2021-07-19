from typing import SupportsAbs
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from rest_framework import status

from .views import RegisterView, LoginView, UserRetrieveUpdateAPIView
from .models import NewUser


class UserAccountsTest(TestCase):
    def test_super_user(self):
        db = get_user_model()
        superuser = db.objects.create_superuser(
            email="test@gmail.com", role=1, password="password"
        )
        self.assertEqual(superuser.email, "test@gmail.com")
        self.assertEqual(superuser.role, 1)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertEqual(str(superuser), "test@gmail.com")

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="email@gmail.com", role=1, password="password", is_superuser=False
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="email@gmail.com", role=1, password="password", is_staff=False
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="email@gmail.com", role=1, password="password", is_active=False
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email="", role=1, password="password", is_superuser=True
            )

    def test_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            email="normal_user@gmail.com", role=2, password="password"
        )
        self.assertEqual(user.email, "normal_user@gmail.com")
        self.assertEqual(user.role, 2)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(email="", role=2, password="ps")


factory = APIRequestFactory()


class TestUserViews(APITestCase):
    def test_register_view(self):
        data = {"email": "bolot.jusupekovv@gmail.com", "password": "password"}
        request = factory.post("/api/register/", data, format="json")
        response = RegisterView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_view(self):
        user = NewUser.objects.create_user(
            email="testuser@gmail.com", password="password"
        )
        user.is_verified = True
        user.save()
        data = {"email": "testuser@gmail.com", "password": "password"}
        request = factory.post("/api/login/", data, format="json")
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile(self):
        user = NewUser.objects.create_user(
            email="testuser@gmail.com", password="password"
        )
        request = factory.get("/api/user/profile/")
        force_authenticate(request, user=user)
        response = UserRetrieveUpdateAPIView.as_view()(request)

        request2 = factory.put(
            "/api/user/profile/", {"password": "newpassword"}, format="json"
        )
        force_authenticate(request2, user=user)
        response2 = UserRetrieveUpdateAPIView.as_view()(request2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
