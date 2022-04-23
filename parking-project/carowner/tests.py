from unittest import TestCase

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
import users
from carowner.models import ParkingMonitor, CarOwner
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
                         data={'parkingName': 'mmd', 'isPrivate': True, 'capacity': 5000, 'pricePerHour': 4500, 'validationStatus': 'V'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'saeed', 'isPrivate': True, 'capacity': 1000, 'pricePerHour': 6000, 'validationStatus': 'V'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'roozbeh', 'isPrivate': True, 'capacity': 8000, 'pricePerHour': 100, 'validationStatus': 'V'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'bakh', 'isPrivate': True, 'capacity': 500, 'pricePerHour': 200, 'validationStatus': 'V'})
        self.client.post(add_parking_url,
                         data={'parkingName': 'mmdbfrs', 'isPrivate': True, 'capacity': 7000, 'pricePerHour': 50, 'validationStatus': 'V'})

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
