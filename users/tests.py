from typing import SupportsAbs
from django.test import TestCase
from django.contrib.auth import get_user_model

class UserAccountsTest(TestCase):

    def test_super_user(self):
        db = get_user_model()
        superuser = db.objects.create_superuser(email='test@gmail.com',role=1, password='password')
        self.assertEqual(superuser.email , 'test@gmail.com')
        self.assertEqual(superuser.role, 1)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertEqual(str(superuser), 'test@gmail.com')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='email@gmail.com', role=1, 
                password='password', is_superuser=False
            )
        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='email@gmail.com', role=1,
                password='password', is_staff=False
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='email@gmail.com',role=1, 
                password='password', is_active=False
            )

        with self.assertRaises(ValueError):
            db.objects.create_superuser(
                email='', role=1,
                password='password', is_superuser=True
            )

    def test_user(self):
        db = get_user_model()
        user = db.objects.create_user(email='normal_user@gmail.com', role=2, password='password')
        self.assertEqual(user.email, 'normal_user@gmail.com')
        self.assertEqual(user.role, 2)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

        with self.assertRaises(ValueError):
            db.objects.create_user(email='',role=2, password='ps')