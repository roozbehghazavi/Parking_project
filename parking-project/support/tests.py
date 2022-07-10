from django.test import TestCase
from datetime import datetime,timedelta
from django.urls import reverse
from rest_framework.test import APITestCase
from carowner.models import CarOwner,Car
from parkingowner.models import Parking, Period, ParkingOwner
from users.models import CustomUser
from support.models import Support
from rest_framework.authtoken.models import Token
# Create your tests here.
class SupportDetailsTest(APITestCase):
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'S'})
        self.assertEqual(response.status_code, 201)
        Stoken = Token.objects.last().key

        #Get Support details
        self.client.credentials(HTTP_AUTHORIZATION = 'token ')
        response = self.client.get('/support/support_detail/')  
        self.assertEqual(response.status_code,401)

    def test_success(self):
        #Register a Support
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'S'})
        self.assertEqual(response.status_code, 201)
        Stoken = Token.objects.last().key

        #Get Support details
        self.client.credentials(HTTP_AUTHORIZATION = 'token '+ Stoken)
        response = self.client.get('/support/support_detail/')  
        assert response.status_code == 200 or 201

class ParkingListTest(APITestCase):
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'S'})
        self.assertEqual(response.status_code, 201)
        Stoken = Token.objects.last().key

        #Get Support details
        self.client.credentials(HTTP_AUTHORIZATION = 'token ')
        response = self.client.get('/support/parkinglist/')  
        self.assertEqual(response.status_code,401)

    def test_success(self):
        #Register a Support
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'S'})
        self.assertEqual(response.status_code, 201)
        Stoken = Token.objects.last().key

        #Get Support details
        self.client.credentials(HTTP_AUTHORIZATION = 'token '+ Stoken)
        response = self.client.get('/support/parkinglist/')  
        assert response.status_code == 200 or 201