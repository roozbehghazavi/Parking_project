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
class ParkingListCarOwnerTest(APITestCase):
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #/// carowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        Ctoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking list unauthorized
        self.client.credentials(HTTP_AUTHORIZATION = 'token ')
        response = self.client.get('/carowner/parkinglist/')  
        self.assertEqual(response.status_code,401)

    def test_success(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #/// carowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        Ctoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking list
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)
        response = self.client.get('/carowner/parkinglist/')  
        assert response.status_code == 200 or 201

class ParkingListParkingOwnerTest(APITestCase):
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking list unauthorized
        self.client.credentials(HTTP_AUTHORIZATION = 'token ')
        response = self.client.get('/parkingowner/parkinglist/')  
        self.assertEqual(response.status_code,401)

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
        response = self.client.get('/parkingowner/parkinglist/')  
        assert response.status_code == 200 or 201
class ParkingDetailsParkingOwnerTest(APITestCase):
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking details
        response = self.client.get('/parkingowner/parkingdetail/', {'id':'2'})  
        self.assertEqual(response.status_code,404)

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
        assert response.status_code == 200 or 201


class ParkingDetailsCarOwnerTest(APITestCase):
    def test_failed(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Register a Carowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        Ctoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking details
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)
        response = self.client.get('/carowner/parkingdetail/', {'id':'2'})  
        self.assertEqual(response.status_code,404)

    def test_success(self):
        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key

        #Register a Carowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        Ctoken = Token.objects.last().key

        #Create a Parking
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'42.345'})
        assert response.status_code == 200 or 201

        #Get parking details
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)
        response = self.client.get('/carowner/parkingdetail/', {'id':'1'})  
        assert response.status_code == 200 or 201

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

class ParkingUpdateTest(APITestCase):
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
        response = self.client.put('/parkingowner/updateparking/', {'id':'1','parkingName':'miladnoor'})
        self.assertEqual(Parking.objects.first().parkingName, 'Lidoma')
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
        response = self.client.get('/parkingowner/income/',{'parkingId':'1','interval':'month'})
        assert response.status_code == 200 or 201

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
        
        #income
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.get('/parkingowner/income/',{'parkingId':'2','interval':'month'})
        assert response.status_code == 404


class OverallCustomersTest(APITestCase):
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
        response = self.client.get('/parkingowner/allcustomers/',{'parkingId':'1','interval':'month'})
        assert response.status_code == 200 or 201

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
        
        #income
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
        response = self.client.get('/parkingowner/allcustomers/',{'parkingId':'2','interval':'month'})
        assert response.status_code == 404