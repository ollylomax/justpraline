from django.test import TestCase
import unittest
from django.test import Client


# Unit test to check cart view
class CartViewTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/cart/')
        self.assertEqual(response.status_code, 200)
