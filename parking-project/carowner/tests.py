from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient    
from rest_framework.test import APITestCase
import users
# Create your tests here.


class APITest(APITestCase):
    def setUp(self):
        
        self.client = APIClient()
        response = self.client.post('/users/rest-auth/registration/', {'email':'C@gmail.com','password1':'mmd12345','password2':'mmd12345','role':'C'})

    def test_get_current_user(self):
        pass