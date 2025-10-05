import unittest
import json

import sys
import os

current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file))
sys.path.insert(0, project_root)

from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test variables"""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create tables
        db.create_all()
        
        # Test user data
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
    
    def tearDown(self):
        """Clean up after tests"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_registration(self):
        """Test user registration works correcty"""
        response = self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        # Check if the request was successful
        self.assertEqual(response.status_code, 201)
        
        # Check if the user was created in the database
        user = User.query.filter_by(username=self.user_data['username']).first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_data['email'])
        
        # Print success message
        print("\n[TEST PASSED] test_user_registration: User registration works correctly.")
    
    def test_user_registration_missing_fields(self):
        """Test user registration with missing fields"""
        incomplete_data = {
            'username': 'testuser',
            'email': 'test@example.com'
            # Missing password
        }
        
        response = self.client.post(
            '/auth/register',
            data=json.dumps(incomplete_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 400)
        
        # Print success message
        print("\n[TEST PASSED] test_user_registration_missing_fields: User registration with missing fields correctly fails.")
    
    def test_user_registration_duplicate_username(self):
        """Test user registration with duplicate username"""
        # Register the first user
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        # Try to register the same username again
        duplicate_data = self.user_data.copy()
        duplicate_data['email'] = 'different@example.com'
        
        response = self.client.post(
            '/auth/register',
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username already exists', str(response.data))
        
        # Print success message
        print("\n[TEST PASSED] test_user_registration_duplicate_username: User registration with duplicate username correctly fails.")
    
    def test_user_registration_duplicate_email(self):
        """Test user registration with duplicate email"""
        # Register the first user
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        # Try to register the same email again
        duplicate_data = self.user_data.copy()
        duplicate_data['username'] = 'differentuser'
        
        response = self.client.post(
            '/auth/register',
            data=json.dumps(duplicate_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 400)
        self.assertIn('Email already exists', str(response.data))
        
        # Print success message
        print("\n[TEST PASSED] test_user_registration_duplicate_email: User registration with duplicate email correctly fails.")
    
    def test_user_login(self):
        """Test user login works correctly"""
        # Register a user first
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        # Login with the same credentials
        login_data = {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        }
        
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Check if the request was successful
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains a token
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertIn('user', data)
        
        # Print success message
        print("\n[TEST PASSED] test_user_login: User login works correctly.")
    
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        # Register a user first
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        # Login with wrong password
        login_data = {
            'username': self.user_data['username'],
            'password': 'wrongpassword'
        }
        
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', str(response.data))
        
        # Print success message
        print("\n[TEST PASSED] test_user_login_invalid_credentials: User login with invalid credentials correctly fails.")
    
    def test_user_login_nonexistent_user(self):
        """Test login with a non-existent user"""
        login_data = {
            'username': 'nonexistent',
            'password': 'password123'
        }
        
        response = self.client.post(
            '/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid username or password', str(response.data))
        
        # Print success message
        print("\n[TEST PASSED] test_user_login_nonexistent_user: Login with a non-existent user correctly fails.")
    
    def test_get_profile(self):
        """Test getting user profile"""
        # Register and login a user
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }),
            content_type='application/json'
        )
        
        self.assertEqual(login_response.status_code, 200)
        token = json.loads(login_response.data)['token']
        self.assertIsNotNone(token)
        
        # Get profile
        response = self.client.get(
            '/auth/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Check if the request was successful
        self.assertEqual(response.status_code, 200)
        
        # Check if the response contains user data
        data = json.loads(response.data)
        self.assertEqual(data['username'], self.user_data['username'])
        self.assertEqual(data['email'], self.user_data['email'])
        
        # Print success message
        print("\n[TEST PASSED] test_get_profile: Getting user profile works correctly.")
    
    def test_get_profile_without_token(self):
        """Test getting user profile without token"""
        response = self.client.get('/auth/profile')
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        
        # Print success message
        print("\n[TEST PASSED] test_get_profile_without_token: Getting user profile without token correctly fails.")
    
    def test_update_profile(self):
        """Test updating user profile"""
        # Register and login a user
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }),
            content_type='application/json'
        )
        
        self.assertEqual(login_response.status_code, 200)
        token = json.loads(login_response.data)['token']
        self.assertIsNotNone(token)
        
        # Update profile
        update_data = {
            'email': 'updated@example.com',
            'password': 'newpassword123'
        }
        
        response = self.client.put(
            '/auth/profile',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Check if the request was successful
        self.assertEqual(response.status_code, 200)
        
        # Check if the profile was updated
        profile_response = self.client.get(
            '/auth/profile',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        self.assertEqual(profile_response.status_code, 200)
        profile_data = json.loads(profile_response.data)
        self.assertEqual(profile_data['email'], update_data['email'])
        
        # Print success message
        print("\n[TEST PASSED] test_update_profile: Updating user profile works correctly.")
    
    def test_update_profile_without_token(self):
        """Test updating user profile without token"""
        update_data = {
            'email': 'updated@example.com'
        }
        
        response = self.client.put(
            '/auth/profile',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        
        # Print success message
        print("\n[TEST PASSED] test_update_profile_without_token: Updating user profile without token correctly fails.")
    
    def test_get_users(self):
        """Test getting all users as non-admin"""
        # Register regular user
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        # Login as regular user
        login_response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }),
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['token']
        
        # Try to get users
        response = self.client.get(
            '/auth/users',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Check if the request was denied
        self.assertEqual(response.status_code, 403)
        
        # Print success message
        print("\n[TEST PASSED] test_get_users: Getting all users as non-admin correctly fails.")
    
    def test_get_users_without_token(self):
        """Test getting all users without token"""
        response = self.client.get('/auth/users')
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        
        # Print success message
        print("\n[TEST PASSED] test_get_users_without_token: Getting all users without token correctly fails.")
    
    def test_update_user(self):
        """Test updating user as non-admin"""
        # Register regular users
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        self.client.post(
            '/auth/register',
            data=json.dumps({
                'username': 'user2',
                'email': 'user2@example.com',
                'password': 'password123'
            }),
            content_type='application/json'
        )
        
        # Login as first regular user
        login_response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }),
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['token']
        
        # Get the second user's ID
        users_response = self.client.get(
            '/auth/users',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        users = json.loads(users_response.data)['users']
        second_user_id = next(user['id'] for user in users if user['username'] == 'user2')
        
        # Try to update the second user
        update_data = {
            'is_active': False
        }
        
        response = self.client.put(
            f'/auth/users/{second_user_id}',
            data=json.dumps(update_data),
            content_type='application/json',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Check if the request was denied
        self.assertEqual(response.status_code, 403)
        
        # Print success message
        print("\n[TEST PASSED] test_update_user: Updating user as non-admin correctly fails.")
    
    
    def test_update_user_without_token(self):
        """Test updating user without token"""
        update_data = {
            'is_active': False
        }
        
        response = self.client.put(
            '/auth/users/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        
        # Print success message
        print("\n[TEST PASSED] test_update_user_without_token: Updating user without token correctly fails.")
    
    def test_logout(self):
        """Test user logout"""
        # Register and login a user
        self.client.post(
            '/auth/register',
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        
        login_response = self.client.post(
            '/auth/login',
            data=json.dumps({
                'username': self.user_data['username'],
                'password': self.user_data['password']
            }),
            content_type='application/json'
        )
        
        token = json.loads(login_response.data)['token']
        
        # Logout
        response = self.client.post(
            '/auth/logout',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        # Check if the request was successful
        self.assertEqual(response.status_code, 200)
        self.assertIn('Logout successful', str(response.data))
        
        # Print success message
        print("\n[TEST PASSED] test_logout: User logout works correctly.")
    
    def test_logout_without_token(self):
        """Test user logout without token"""
        response = self.client.post('/auth/logout')
        
        # Check if the request failed
        self.assertEqual(response.status_code, 401)
        
        # Print success message
        print("\n[TEST PASSED] test_logout_without_token: User logout without token correctly fails.")

if __name__ == '__main__':
    unittest.main()
    
