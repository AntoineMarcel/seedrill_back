from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Sequence
from rest_framework.test import force_authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class AccountTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create(username="admin")
        token = Token.objects.get(user__username='admin')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_sequence(self):
        """
        Ensure we can create a new sequence object.
        """
        url = reverse('sequence')
        data = {  
            "data": {  
                "senderName": "Your name",  
                "subjectEmail": "Hi guys",  
                "replyEmail": "test@test.fr"  
            }  
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sequence.objects.count(), 1)
        self.assertEqual(Sequence.objects.get().senderName, 'Your name')
        self.assertEqual(Sequence.objects.get().subjectEmail, 'Hi guys')
        self.assertEqual(Sequence.objects.get().replyEmail, 'test@test.fr')

    def test_wrong_create_sequence1(self):
        """
        Ensure we can't create a wrong new sequence object. Missing parameter.
        """
        url = reverse('sequence')
        data = {  
            "data": {  
                "senderName": "Your name",  
                "subjectEmail": "Hi guys",  
            }  
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sequence.objects.count(), 0)

    def test_wrong_create_sequence2(self):
        """
        Ensure we can't create a wrong new sequence object. Wrong typing parameter
        """
        url = reverse('sequence')
        data = {  
            "data": {  
                "senderNamee": "Your name",  
                "subjectEmail": "Hi guys",  
                "replyEmail": "test@test.fr"  
            }  
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sequence.objects.count(), 0)

    def test_wrong_create_sequence3(self):
        """
        Ensure we can't create a wrong new sequence object. Wrong email
        """
        url = reverse('sequence')
        data = {  
            "data": {  
                "senderName": "Your name",  
                "subjectEmail": "Hi guys",  
                "replyEmail": "testtest.fr"  
            }  
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Sequence.objects.count(), 0)