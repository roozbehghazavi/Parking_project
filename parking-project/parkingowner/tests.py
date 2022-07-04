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
class ParkingDetailsTest(APITestCase):
    def test_success(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking details
        response = self.client.get('/parkingowner/parkingdetail/', {'id':'1'})  
        self.assertEqual(response.status_code,404)

class ParkingCreateTest(APITestCase):
    def test_success(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})  
        

        self.assertEqual(Parking.objects.first().parkingName, 'Lidoma')
        self.assertEqual(Parking.objects.first().capacity,1000)
    
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})  
        
        self.assertNotEqual(Parking.objects.first().capacity,1001)

class ParkingValidationTest(APITestCase):
    def test_success(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})

        #Validate a Parking  
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.put('/parkingowner/updateparking/', {'id':'1','validationStatus':'V'})

        self.assertEqual(Parking.objects.first().validationStatus, 'I')

    
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        #Validate a Parking  
        response = self.client.put('/parkingowner/updateparking/', {'id':'1','validationStatus':'V'})

        self.assertNotEqual(Parking.objects.first().validationStatus, 'P')

class OverallIncomeTest(APITestCase):
    def test_success(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        
        #Validate a Parking  
        response = self.client.put('/parkingowner/updateparking/', {'id':'1','validationStatus':'V'})
        
        #income
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.get('/parkingowner/income/',{'start':'2022-05-01','end':'2022-05-25'})

        