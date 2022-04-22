from http import client
from urllib import response
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient    
from rest_framework.test import APITestCase
import users
from users.models import CustomUser
from rest_framework.authtoken.models import Token
# Create your tests here.


class RegistrationTest(APITestCase):

    def test(self):  
        self.client = APIClient()
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        assert response.status_code == 201



class LoginTest(APITestCase):

    def test_check_user(self):
        self.client = APIClient()
        self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertTrue(self.client.login(email='mmdbfrst@gmail.com',password='affarin234'))
        


class EditProfileTest(APITestCase):

    def test_edit_profile(self):
        self.client = APIClient()
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        token = Token.objects.first().key

        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + token)

        url = reverse('edit-profile')

        self.client.put(url, {'firstName' : 'mmd', 'lastName':'bakhfazian'},format='json')

        self.assertEqual(CustomUser.objects.first().firstName, 'mmd')
        self.assertEqual(CustomUser.objects.first().lastName, 'bakhfazian')
    
class PhonenumberOtpTest(APITestCase):
    def test_phonenumber_otp(self):
        self.client=APIClient()
        
        #register User
        register = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'P','phoneNumber':'09123456789'})
        self.assertEqual(register.status_code, 201)

        #Get credentials
        token = Token.objects.first().key
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + token)

        #Put phoneNumber
        url = reverse('edit-profile')
        self.client.put(url, {'phoneNumber' : '09123456789'})
        self.assertEqual(CustomUser.objects.first().phoneNumber, '09123456789')

        #OTP test
        response = self.client.post('/users/otpvalidation/',{'phoneNumber':'09123456789'})
        self.assertEqual(response.status_code, 200)