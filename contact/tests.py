from django.test import TestCase
import unittest
from django.test import Client


# Unit test to check contact view
class ContactViewTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/contact/')
        self.assertEqual(response.status_code, 200)
