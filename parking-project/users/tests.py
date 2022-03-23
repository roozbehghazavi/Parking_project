from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient    
from rest_framework.test import APITestCase
import users
from users.models import CustomUser
# Create your tests here.


class RegistrationTest(APITestCase):

    def test(self):  
        self.client = APIClient()
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        assert response.status_code == 201



class CheckUserViewTest(APITestCase):

    def test_check_user(self):
        self.client = APIClient()
        user = CustomUser.objects.create_user('username', 'Pas$w0rd')
        self.assertTrue(self.client.login(username='username', password='Pas$w0rd'))