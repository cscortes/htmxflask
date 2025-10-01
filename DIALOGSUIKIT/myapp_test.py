#!/usr/bin/env python3

import unittest
from myapp import app, submissions

class DialogsUIKitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Clear submissions before each test
        submissions.clear()

    def test_index_loads(self):
        """Test that the index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1 class="uk-heading-medium uk-text-center">HTMX UIKit Modal Dialogs Example</h1>', response.data)

    def test_modal_endpoint_loads(self):
        """Test that the modal endpoint returns modal HTML"""
        response = self.client.get('/modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<div id="modal" class="uk-modal"', response.data)
        self.assertIn(b'<h2 class="uk-modal-title">Modal Dialog</h2>', response.data)

    def test_modal_contains_form(self):
        """Test that modal contains the expected form elements"""
        response = self.client.get('/modal')
        self.assertIn(b'<form hx-post="/submit"', response.data)
        self.assertIn(b'class="uk-input"', response.data)
        self.assertIn(b'name="name"', response.data)
        self.assertIn(b'<button type="submit"', response.data)

    def test_modal_contains_hyperscript(self):
        """Test that modal contains Hyperscript for animations"""
        response = self.client.get('/modal')
        self.assertIn(b'_="on submit take .uk-open from #modal"', response.data)
        self.assertIn(b'_="on click take .uk-open from #modal', response.data)

    def test_submit_with_valid_name(self):
        """Test form submission with valid name"""
        response = self.client.post('/submit', data={'name': 'John Doe'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, John Doe! Your submission has been saved.', response.data)
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0]['name'], 'John Doe')

    def test_submit_with_empty_name(self):
        """Test form submission with empty name"""
        response = self.client.post('/submit', data={'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter your name.', response.data)
        self.assertEqual(len(submissions), 0)

    def test_submit_with_whitespace_name(self):
        """Test form submission with whitespace-only name"""
        response = self.client.post('/submit', data={'name': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter your name.', response.data)
        self.assertEqual(len(submissions), 0)

    def test_multiple_submissions(self):
        """Test multiple form submissions accumulate"""
        # First submission
        response1 = self.client.post('/submit', data={'name': 'Alice'})
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(submissions), 1)

        # Second submission
        response2 = self.client.post('/submit', data={'name': 'Bob'})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(submissions), 2)

        # Check both submissions are present
        names = [sub['name'] for sub in submissions]
        self.assertIn('Alice', names)
        self.assertIn('Bob', names)

    def test_clear_submissions(self):
        """Test clearing all submissions"""
        # Add some submissions first
        submissions.append({'name': 'Test User', 'timestamp': 'Now'})
        submissions.append({'name': 'Another User', 'timestamp': 'Now'})
        self.assertEqual(len(submissions), 2)

        # Clear submissions
        response = self.client.post('/clear')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All submissions cleared!', response.data)
        self.assertEqual(len(submissions), 0)

    def test_index_with_submissions(self):
        """Test index page displays submissions when present"""
        # Add a submission
        submissions.append({'name': 'Test User', 'timestamp': 'Just now'})
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2 class="uk-heading-small">Recent Submissions</h2>', response.data)
        self.assertIn(b'Test User', response.data)
        # Check for hx-confirm attribute when submissions exist
        self.assertIn(b'hx-confirm="Are you sure you want to clear all submissions?"', response.data)

    def test_index_without_submissions(self):
        """Test index page when no submissions exist"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'<h2 class="uk-heading-small">Recent Submissions</h2>', response.data)

    def test_index_contains_htmx_attributes(self):
        """Test that index.html contains necessary HTMX attributes"""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for hx-get attribute
        self.assertIn('hx-get="/modal"', html)

        # Check for hx-target attribute
        self.assertIn('hx-target="#modals-here"', html)

        # Check for hx-post attribute (in the educational section)
        self.assertIn('hx-post="/submit"', html)

    def test_index_contains_uikit_classes(self):
        """Test that index.html contains UIKit CSS classes"""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for UIKit classes
        self.assertIn('uk-button uk-button-primary', html)
        self.assertIn('uk-container', html)
        self.assertIn('uk-card', html)
        self.assertIn('uk-grid', html)

    def test_index_contains_hyperscript(self):
        """Test that index.html contains Hyperscript for animations"""
        response = self.client.get('/')
        self.assertIn(b'_="on htmx:afterOnLoad wait 10ms then add .uk-open to #modal"', response.data)

    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = self.client.get('/')

        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-XSS-Protection'), '1; mode=block')
        self.assertIn('max-age=31536000', response.headers.get('Strict-Transport-Security'))
        self.assertIn("default-src 'self'", response.headers.get('Content-Security-Policy'))

    def test_favicon_present(self):
        """Test that favicons are linked in the HTML"""
        response = self.client.get('/')
        self.assertIn(b'<link rel="icon" href="/static/img/favicon.svg" type="image/svg+xml">', response.data)
        self.assertIn(b'<link rel="alternate icon" href="/static/img/favicon-emoji.svg" type="image/svg+xml">', response.data)

    def test_modal_form_has_required_attribute(self):
        """Test that the modal form input has required attribute"""
        response = self.client.get('/modal')
        self.assertIn(b'required', response.data)

    def test_modal_contains_close_button(self):
        """Test that modal contains close button with proper attributes"""
        response = self.client.get('/modal')
        self.assertIn(b'id="cancelButton"', response.data)
        self.assertIn(b'type="button"', response.data)
        self.assertIn(b'uk-button uk-button-default', response.data)

    def test_submit_with_special_characters(self):
        """Test form submission with special characters in name"""
        special_name = "Test & <script>alert('xss')</script>"
        response = self.client.post('/submit', data={'name': special_name})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, Test & <script>alert(\'xss\')</script>! Your submission has been saved.', response.data)
        self.assertEqual(len(submissions), 1)
        self.assertEqual(submissions[0]['name'], special_name)

    def test_index_contains_how_it_works_section(self):
        """Test that index contains educational 'How It Works' section"""
        response = self.client.get('/')
        self.assertIn(b'<h2 class="uk-heading-small">How It Works</h2>', response.data)
        self.assertIn(b'HTMX Integration', response.data)
        self.assertIn(b'UIKit Features', response.data)

    def test_index_contains_htmx_patterns_section(self):
        """Test that index contains HTMX patterns demonstration section"""
        response = self.client.get('/')
        self.assertIn(b'<h2 class="uk-heading-small">HTMX Patterns Demonstrated</h2>', response.data)
        self.assertIn(b'Dynamic Loading', response.data)
        self.assertIn(b'Form Submission', response.data)
        self.assertIn(b'Confirmation', response.data)

if __name__ == '__main__':
    unittest.main()
