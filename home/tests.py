from django.test import TestCase
import unittest
from django.test import Client


# Unit test to test root view
class HomeViewTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/')
        self.assertEqual(response.status_code, 200)
