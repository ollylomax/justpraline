from django.test import TestCase
import unittest
from django.test import Client


# Unit test to check products view
class ProductsViewTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/products/')
        self.assertEqual(response.status_code, 200)


# Unit test to check product_detail view
class ProductDetailViewTest(unittest.TestCase):
    def test_details(self):
        client = Client()
        response = client.get('/products/1/')
        self.assertEqual(response.status_code, 200)
