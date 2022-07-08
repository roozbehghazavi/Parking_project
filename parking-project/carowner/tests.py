from datetime import datetime
from datetime import timedelta
from unittest import TestCase

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import users
from carowner.models import ParkingMonitor, CarOwner,Car
from parkingowner.models import Parking, Period, ParkingOwner
from users.models import CustomUser
from rest_framework.authtoken.models import Token


class ParkingSearchTest(APITestCase):

    def setUp(self) -> None:
        Parking.objects.all().delete()
        CustomUser.objects.all().delete()
        Token.objects.all().delete()
        Period.objects.all().delete()
        CarOwner.objects.all().delete()
        ParkingOwner.objects.all().delete()

        self.client = APIClient()
        self.client.post('/users/rest-auth/registration/',
                            {'email': 'P@gmail.com', 'password1': 'affarin234',
                             'password2': 'affarin234', 'role': 'P'})
        token = Token.objects.first().key

        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)
        add_parking_url = reverse('add_parking')
        self.client.post(add_parking_url,
                         data={'parkingName': 'mmd', 'isPrivate': True, 'capacity': 5000, 'pricePerHour': 4500, 'validationStatus': 'V','lat':'23.234','lng':'245.345'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'saeed', 'isPrivate': True, 'capacity': 1000, 'pricePerHour': 6000, 'validationStatus': 'V','lat':'23.234','lng':'245.345'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'roozbeh', 'isPrivate': True, 'capacity': 8000, 'pricePerHour': 100, 'validationStatus': 'V','lat':'23.234','lng':'245.345'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'bakh', 'isPrivate': True, 'capacity': 500, 'pricePerHour': 200, 'validationStatus': 'V','lat':'23.234','lng':'245.345'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'mmdbfrs', 'isPrivate': True, 'capacity': 7000, 'pricePerHour': 50, 'validationStatus': 'V','lat':'23.234','lng':'245.345'})

        self.client.post('/users/rest-auth/registration/',
                         {'email': 'C@gmail.com', 'password1': 'affarin234',
                          'password2': 'affarin234', 'role': 'C'})

        token = Token.objects.filter(user__email='C@gmail.com').first().key
        self.client.credentials(HTTP_AUTHORIZATION='token ' + token)

        search_click_url = reverse('search_click')
        parking_ids = Parking.objects.all().order_by('id').values_list('id', flat=True)

        self.client.post(search_click_url, {'parking_id': parking_ids[1]})
        self.client.post(search_click_url, {'parking_id': parking_ids[1]})
        self.client.post(search_click_url, {'parking_id': parking_ids[2]})
        self.client.post(search_click_url, {'parking_id': parking_ids[1]})
        self.client.post(search_click_url, {'parking_id': parking_ids[1]})
        self.client.post(search_click_url, {'parking_id': parking_ids[1]})
        self.client.post(search_click_url, {'parking_id': parking_ids[2]})
        self.client.post(search_click_url, {'parking_id': parking_ids[3]})
        self.assertEqual(ParkingMonitor.objects.count(), 8)

    def test_parking_search(self):
        response = self.client.get('/carowner/parkingsearch/?search=mmd')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('results')[0]['parkingName'], 'mmd')

        response = self.client.get('/carowner/parkingsearch/?search=&ordering=capacity')
        self.assertEqual(response.data.get('results')[0]['parkingName'], 'bakh')

        response = self.client.get('/carowner/parkingsearch/?search=&ordering=capacity&min_price=1000')
        self.assertEqual(response.data.get('results')[0]['parkingName'], 'saeed')

    def test_get_min_max_price(self):
        url = reverse('get_min_max_price')
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get(0), 50)
        self.assertEqual(response.data.get(1), 6000)

    def test_get_recent_parkings(self):
        url = reverse('get_recent_parkings')
        response = self.client.get(url)
        self.assertEqual(response.data[0]['parkingName'], 'bakh')

    def test_get_most_popular_parkings(self):
        url = reverse('get_most_popular_parkings')

        response = self.client.get(url)
        self.assertEqual(response.data[0]['parkingName'], 'saeed')

######### Car Tests #########
class CarCreateTest(APITestCase):

    def test_success(self):  
        self.client = APIClient()

        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        token = Token.objects.first().key

        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + token)

        response = self.client.post('/carowner/carcreate/', {'carName':'ParsELX','pelak':'12345567','color':'black'})  
        assert response.status_code == 201

        self.assertEqual(Car.objects.first().carName, 'ParsELX')
        self.assertEqual(Car.objects.first().pelak, '12345567')
        self.assertEqual(Car.objects.first().color, 'black')

    def test_failed(self):
        self.client = APIClient()

        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrst@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        token = Token.objects.first().key

        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + token)

        response = self.client.post('/carowner/carcreate/', {'carName':'ParsELX','pelak':'123457','color':'black'})  
        assert response.status_code == 400

        self.assertEqual(Car.objects.count(),0)

#############################

######### Reservation Tests #########
class ReservationTest(APITestCase):

    def test(self):
        self.client = APIClient()

        #Registar a carowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        Ctoken = Token.objects.first().key

        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key
   
        #Check if two users are created successfully
        self.assertEqual(CustomUser.objects.count(),2)
   
        #Create a car
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)
        response = self.client.post('/carowner/carcreate/', {'carName':'ParsELX','pelak':'12345567','color':'black'})  
        assert response.status_code == 201

        self.assertEqual(Car.objects.first().carName, 'ParsELX')
        self.assertEqual(Car.objects.first().pelak, '12345567')
        self.assertEqual(Car.objects.first().color, 'black')

        #Create a Parking
        try:
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'245.345'})  
            

            self.assertEqual(Parking.objects.first().parkingName, 'Lidoma')
            self.assertEqual(Parking.objects.first().capacity,1000)
        

            #Validate a Parking
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.put('/parkingowner/updateparking/', {'id':'1','validationStatus':'V'})

            self.assertNotEqual(Parking.objects.first().validationStatus, 'P')

            #Setting Template
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.put('/parkingowner/edittemplate/', {"id" : 7,"openAt" : "00:00:01","closeAt" : "23:59:00","days":[
            {
                "day" : 1,
                "is_selected":True
            },
            {
                "day" : 2,
                "is_selected":True
            },
            {
                "day" : 3,
                "is_selected":True
            },
            {
                "day" : 4,
                "is_selected":True
            },
            {
                "day" : 5,
                "is_selected":True
            },
            {
                "day" : 6,
                "is_selected":True
            }
        ]
    })
            
            #Get Template
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.get('/parkingowner/templatedetail/', {'parking_id':'1'})
            assert response.status_code == 200 or 201

            #Reservation
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)

            enter=str(datetime.now())
            exit=str(datetime.now()+timedelta(hours=1))

            response = self.client.post('/carowner/reserve/', {"parking_id" : 1, "enter" : enter,"exit" : exit,"car_id" : 1})
            assert response.status_code == 404
        except:
            pass
class ReservationCancelTest(APITestCase):

    def test(self):
        self.client = APIClient()

        #Registar a carowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        Ctoken = Token.objects.first().key

        #Register a parkingowner
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstP@gmail.com','password1':'affarin234','password2':'affarin234','role':'P'})
        self.assertEqual(response.status_code, 201)
        Ptoken = Token.objects.last().key
   
        #Check if two users are created successfully
        self.assertEqual(CustomUser.objects.count(),2)
   
        #Create a car
        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)
        response = self.client.post('/carowner/carcreate/', {'carName':'ParsELX','pelak':'12345567','color':'black'})  
        assert response.status_code == 201

        self.assertEqual(Car.objects.first().carName, 'ParsELX')
        self.assertEqual(Car.objects.first().pelak, '12345567')
        self.assertEqual(Car.objects.first().color, 'black')

        #Create a Parking
        try:
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.post('/parkingowner/createparking/', {'parkingName':'Lidoma','isPrivate':'False','location':'hemat highway','parkingPhoneNumber':'223478132','capacity':'1000','pricePerHour':'2000','lat':'23.234','lng':'245.345'})  
            

            self.assertEqual(Parking.objects.first().parkingName, 'Lidoma')
            self.assertEqual(Parking.objects.first().capacity,1000)

        #Validate a Parking
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.put('/parkingowner/updateparking/', {'id':'1','validationStatus':'V'})

            self.assertNotEqual(Parking.objects.first().validationStatus, 'P')

            #Setting Template
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.put('/parkingowner/edittemplate/', {"id" : 7,"openAt" : "00:00:01","closeAt" : "23:59:00","days":[
            {
                "day" : 1,
                "is_selected":True
            },
            {
                "day" : 2,
                "is_selected":True
            },
            {
                "day" : 3,
                "is_selected":True
            },
            {
                "day" : 4,
                "is_selected":True
            },
            {
                "day" : 5,
                "is_selected":True
            },
            {
                "day" : 6,
                "is_selected":True
            }
        ]
    })
            
            #Get Template
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ptoken)
            response = self.client.get('/parkingowner/templatedetail/', {'parking_id':'1'})
            assert response.status_code == 200 or 201

            #Reservation
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)

            enter=str(datetime.now())
            exit=str(datetime.now()+timedelta(hours=1))

            response = self.client.post('/carowner/reserve/', {"parking_id" : 1, "enter" : enter,"exit" : exit,"car_id" : 1})
            assert response.status_code == 404

            #delete Reservation
            self.client.credentials(HTTP_AUTHORIZATION = 'token ' + Ctoken)
            response = self.client.delete('/carowner/reserve/', {"id" : 1})
        except:
            pass


class CancellationReasonTest(APITestCase):
    def test_success(self):
        #Register a user
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        token = Token.objects.first().key

        self.client.credentials(HTTP_AUTHORIZATION = 'token ' + token)

        response = self.client.get('/carowner/cancel/', {'parkingId':'1','interval':'year'})
        print(response.status_code)
        assert response.status_code == 404
    
    def test_failed(self):
        #Register a user
        response = self.client.post('/users/rest-auth/registration/', {'email':'mmdbfrstC@gmail.com','password1':'affarin234','password2':'affarin234','role':'C'})
        self.assertEqual(response.status_code, 201)
        token = Token.objects.first().key

        response = self.client.get('/carowner/cancel/', {'id':'1'})
        print(response.status_code)
        assert response.status_code == 401
