#!/usr/bin/env python3
"""
Unit tests for HTMX Inline Validation Example
"""

import unittest
from unittest.mock import patch
from myapp import app


class InlineValidationTestCase(unittest.TestCase):
    """Test cases for inline validation functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_page(self):
        """Test the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('Inline Validation Example', response_text)
        self.assertIn('registration-form', response_text)

    @patch('myapp.time.sleep')  # Mock sleep to speed up tests
    def test_username_validation_success(self, mock_sleep):
        """Test successful username validation."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/username', data={'username': 'validuser123'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-success', response_text)
        self.assertIn('Username is available', response_text)

    @patch('myapp.time.sleep')
    def test_username_validation_taken(self, mock_sleep):
        """Test username validation with taken username."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/username', data={'username': 'admin'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-error', response_text)
        self.assertIn('already taken', response_text)

    @patch('myapp.time.sleep')
    def test_username_validation_too_short(self, mock_sleep):
        """Test username validation with too short username."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/username', data={'username': 'ab'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-error', response_text)
        self.assertIn('at least 3 characters', response_text)

    @patch('myapp.time.sleep')
    def test_email_validation_success(self, mock_sleep):
        """Test successful email validation."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/email', data={'email': 'test@gmail.com'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-success', response_text)
        self.assertIn('Valid email address', response_text)

    @patch('myapp.time.sleep')
    def test_email_validation_invalid_format(self, mock_sleep):
        """Test email validation with invalid format."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/email', data={'email': 'invalid-email'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-error', response_text)
        self.assertIn('valid email address', response_text)

    @patch('myapp.time.sleep')
    def test_password_validation_strong(self, mock_sleep):
        """Test password validation with strong password."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/password', data={'password': 'StrongPass123!'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-success', response_text)
        self.assertIn('Strong password', response_text)

    @patch('myapp.time.sleep')
    def test_password_validation_weak(self, mock_sleep):
        """Test password validation with weak password."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/password', data={'password': 'weakpass'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-error', response_text)
        self.assertIn('Weak password', response_text)

    @patch('myapp.time.sleep')
    def test_confirm_password_match(self, mock_sleep):
        """Test confirm password validation with matching passwords."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/confirm-password',
                                  data={'password': 'test123', 'confirm_password': 'test123'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-success', response_text)
        self.assertIn('Passwords match', response_text)

    @patch('myapp.time.sleep')
    def test_confirm_password_mismatch(self, mock_sleep):
        """Test confirm password validation with mismatched passwords."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/confirm-password',
                                  data={'password': 'test123', 'confirm_password': 'different'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-error', response_text)
        self.assertIn('do not match', response_text)

    @patch('myapp.time.sleep')
    def test_age_validation_success(self, mock_sleep):
        """Test successful age validation."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/age', data={'age': '25'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-success', response_text)
        self.assertIn('Age verified', response_text)

    @patch('myapp.time.sleep')
    def test_age_validation_underage(self, mock_sleep):
        """Test age validation with underage user."""
        mock_sleep.return_value = None

        response = self.client.post('/validate/age', data={'age': '12'})
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('validation-error', response_text)
        self.assertIn('at least 13 years old', response_text)

    @patch('myapp.time.sleep')
    def test_form_submission_success(self, mock_sleep):
        """Test successful form submission."""
        mock_sleep.return_value = None

        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'StrongPass123!',
            'confirm_password': 'StrongPass123!',
            'age': '25'
        }

        response = self.client.post('/submit-form', data=form_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertIn('Registration successful', response_data['message'])

    @patch('myapp.time.sleep')
    def test_form_submission_validation_error(self, mock_sleep):
        """Test form submission with validation errors."""
        mock_sleep.return_value = None

        form_data = {
            'username': '',  # Empty username
            'email': 'invalid-email',
            'password': 'weak',
            'confirm_password': 'weak',
            'age': '10'
        }

        response = self.client.post('/submit-form', data=form_data)
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('errors', response_data)
        self.assertGreater(len(response_data['errors']), 0)

    def test_htmx_attributes_present(self):
        """Test that HTMX attributes are present in the HTML."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for HTMX validation attributes
        self.assertIn('hx-post="/validate/username"', html)
        self.assertIn('hx-trigger="input changed delay:300ms"', html)
        self.assertIn('hx-target="#username-validation"', html)
        self.assertIn('hx-indicator="#username-spinner"', html)

    def test_form_structure(self):
        """Test that the form has correct structure."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for form elements
        self.assertIn('registration-form', html)
        self.assertIn('name="username"', html)
        self.assertIn('name="email"', html)
        self.assertIn('name="password"', html)
        self.assertIn('name="confirm_password"', html)
        self.assertIn('name="age"', html)

    def test_accessibility_attributes(self):
        """Test that accessibility attributes are present."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for ARIA attributes
        self.assertIn('role="alert"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('aria-live="assertive"', html)

    def test_response_content_type(self):
        """Test that responses have correct content type."""
        # Test main page
        response = self.client.get('/')
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

        # Test validation endpoints
        with patch('myapp.time.sleep'):
            response = self.client.post('/validate/username', data={'username': 'test'})
            self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_validation_timing(self):
        """Test that validation endpoints have expected timing."""
        with patch('myapp.time.sleep') as mock_sleep:
            self.client.post('/validate/username', data={'username': 'test'})

            # Check that sleep was called with correct delay
            mock_sleep.assert_called_once()
            args = mock_sleep.call_args[0]
            self.assertAlmostEqual(args[0], 0.2, places=1)


if __name__ == '__main__':
    unittest.main()
