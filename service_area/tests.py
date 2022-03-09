from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from service_area.models import Provider

class ProviderTests(APITestCase):

    def setUp(self):
        self.payload = {
            "name": "zeshan",
            "email": "zee@zee.com",
            "phone_number": "1234567",
            "language": "eng",
            "currency": "USD", 
        }
        response = self.client.post(
            reverse('provider'),
            self.payload,
            format="json")
       	return response


class TestListCreateProvider(ProviderTests):

    def test_create_provider(self):
    	previous_count = Provider.objects.count()
    	response = self.setUp()
    	self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    	self.assertEqual(Provider.objects.count(), previous_count + 1)

    def test_retrieve_all_provider(self):
        response = self.client.get(reverse('provider'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestProviderDeleteUpdate(ProviderTests):

    def test_updates_one_provider(self):
        response = self.setUp()
        url = "/api/provider/" + str(Provider.objects.all().values()[0]['id']) + "/"
        payload={'name': 'zeee',
        'email': 'zee@zee.commm',
        'language': 'eng',
        'currency': 'USD',
        'phone_number': '999999'}
        res = self.client.put(
            url, payload
            )

        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_deletes_one_provider(self):
        res = self.setUp()
        prev_db_count = Provider.objects.all().count()

        url = "/api/provider/" + str(Provider.objects.all().values()[0]['id']) + "/"

        response = self.client.delete(
            url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Provider.objects.all().count(), 1)

