"""
Test User API
"""
from django.urls import reverse

from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserViewTestCase(APITestCase):
    """
    Test View User
    """

    def setUp(self):
        """
        Setup Test
        """
        self.fake = Faker()
        self.email = self.fake.email()
        self.password = self.fake.password()

    def test_create(self):
        """
        Create User
        """
        url = reverse('user-list')

        data = {
            'email': self.email,
            'password': self.password,
            'first_name': 'Jon',
            'last_name': 'Doe',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data.get('email'), self.email)

    def test_update(self):
        """
        Update User
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name='Jon',
            last_name='Doe'
        )
        user.set_password(self.password)
        user.save()

        self.client.force_authenticate(user=user)

        new_email = self.fake.email()
        data = {
            'email': new_email,
        }
        url = reverse('user-detail', kwargs={'pk': 'me'})

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('email'), new_email)

        user = User.objects.get(email=new_email)
        self.assertEqual(user.username, new_email)

    def test_login(self):
        """
        Test login
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name()
        )
        user.set_password(self.password)
        user.save()

        url = '/api/token/'

        data = {
            'username': self.email,
            'password': self.password,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
        Check token is exist
        """
        self.assertIsNotNone(response.data.get('access'))

    def test_get(self):
        """
        Login & request a user
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name()
        )
        user.set_password(self.password)
        user.save()

        url = '/api/token/'

        data = {
            'username': self.email,
            'password': self.password,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
        Creat a new client with a token credential
        """
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        """
        Request a user detail
        """
        url = reverse('user-detail', kwargs={'pk': 'me'})

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('email'), self.email)

    def test_update_after_login(self):
        """
        Login & change a first name of the user
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name=self.fake.first_name(),
            last_name=self.fake.last_name()
        )
        user.set_password(self.password)
        user.save()

        url = '/api/token/'
        data = {
            'username': self.email,
            'password': self.password,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        """
        Creat a new client with a token credential
        """
        token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        first_name = self.fake.first_name()
        data = {'first_name': first_name}

        """
        Patch to the user detail
        """
        url = reverse('user-detail', kwargs={'pk': 'me'})

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('first_name'), first_name)

    def test_get_list_allowed(self):
        """
        Test get list allowed only for staff
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name='Jon',
            last_name='Doe',
            is_staff=True
        )
        user.set_password(self.password)
        user.save()

        self.client.force_authenticate(user=user)

        url = reverse('user-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_forbidden(self):
        """
        Test get list is forbidden because not a staff
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name='Jon',
            last_name='Doe',
        )
        user.set_password(self.password)
        user.save()

        self.client.force_authenticate(user=user)

        url = reverse('user-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_unauthorized(self):
        """
        Test get list is unauthorized because access without login
        """
        user = User.objects.create(
            email=self.email,
            username=self.email,
            first_name='Jon',
            last_name='Doe',
        )
        user.set_password(self.password)
        user.save()

        url = reverse('user-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
