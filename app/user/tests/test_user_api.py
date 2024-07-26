"""
Tests for the user API.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

## noqa NOTE: This gets the url of the funciton create of user app.
CREATE_USER_URLS = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the public  features of the user API. """

    def setUp(self):
        ## noqa NOTE: creates an api client for testing
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        ## noqa NOTE: This calls the api with the url and payload data by the test client.
        res = self.client.post(CREATE_USER_URLS, payload)
        ## noqa NOTE: checks if response status is HTTP_201
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        ## noqa NOTE: checks if user created with the payload email
        user = get_user_model().objects.get(email=payload['email'])
        ## noqa NOTE: checks if user returned has the same password as the payload.
        self.assertTrue(user.check_password(payload['password']))
        ## noqa NOTE: checks if there is not key named 'pasword' in the response data,
        ## noqa this is for security purposes.
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email already exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        ## noqa NOTE: This creates a test user with given payload.
        create_user(**payload)
        ## noqa NOTE: Then try to create another user with the same payload.
        res = self.client.post(CREATE_USER_URLS, payload)
        ## noqa NOTE: This case should return an error message 400, to ensure no duplicate user can be is created.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URLS, payload)
        ## noqa NOTE: checks if return error code if password less than 5 char.
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        ## noqa NOTE: checks for user already exists for email.
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generate token for valid credentials."""
        ## noqa NOTE: creates a user with user_deails
        user_details = {
            'email': 'test@example.com',
            'password': 'test-user-password123',
            'name': 'Test Name',
        }
        create_user(**user_details)
        ## noqa NOTE: uses the same credentials to login user.
        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        ## noqa NOTE: posts the payload to the token url.
        res = self.client.post(TOKEN_URL, payload)
        ## noqa NOTE: checks if response contains token and status 200.
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""

        create_user(email='test@example.com', password='goodpass')

        payload = {
            'email': 'test@example.com',
            'password': 'badpass',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password shows error."""
        payload = {
            'email': 'test@example.com',
            'password': '',
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_unauthorized(self):
        """Test authentication is required for user."""
        res = self.client.get(ME_URL)
        ## noqa NOTE:Making an unauthenticated request.
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        ## noqa NOTE: Create a test user to test.
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name'
        )
        ## noqa NOTE: Create an API testing client.
        self.client = APIClient()
        ## noqa NOTE:Forces the authentication to a specific user,
        ## noqa so that we don't need to do the real authentication.
        ## noqa NOTE: Any request from this client will be authenticated with the specified user.
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged user."""
        ## noqa NOTE: Retrive the details of current authenticated user.
        res = self.client.get(ME_URL)
        ## noqa NOTE: Checks if data is correct.
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed in the me endpoint."""
        ## noqa NOTE: This API's post method is disabled, only put and patch.
        res = self.client.post(ME_URL,{})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated Name',
                   'password': 'newpassword123'
                   }

        res = self.client.patch(ME_URL, payload)

        ## noqa NOTE: Refreshes the user details, not refreshed by default.
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
