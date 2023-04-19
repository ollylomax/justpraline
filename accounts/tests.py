from django.test import TestCase
import unittest
from django.test import Client

# Unit test to check login view
class AccountsLoginTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)


# Unit test to check register view
class AccountsSignupTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)


# Unit test to check reset password view
class AccountsPasswordResetTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/accounts/password/reset/')
        self.assertEqual(response.status_code, 200)
