from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse




class UnitTests(TestCase):
    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    
