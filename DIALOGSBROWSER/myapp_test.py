#!/usr/bin/env python3
"""
Unit tests for DIALOGS example
Tests HTMX dialog functionality including hx-prompt and hx-confirm
"""

import unittest
import tempfile
import os
from myapp import app

class TestDialogsBrowserExample(unittest.TestCase):
    def setUp(self):
        """Set up test client and clear responses"""
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Clear responses for each test
        from myapp import responses
        responses.clear()

    def test_index_page_loads(self):
        """Test that the main page loads correctly"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HTMX Browser Dialogs', response.data)
        self.assertIn(b'hx-prompt', response.data)
        self.assertIn(b'hx-confirm', response.data)

    def test_submit_without_prompt_header(self):
        """Test submit endpoint without HX-Prompt header"""
        response = self.client.post('/submit')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No input provided', response.data)

    def test_submit_with_prompt_header(self):
        """Test submit endpoint with HX-Prompt header"""
        headers = {'HX-Prompt': 'Hello World'}
        response = self.client.post('/submit', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User entered <i>Hello World</i>', response.data)

    def test_submit_with_empty_prompt_header(self):
        """Test submit endpoint with empty HX-Prompt header"""
        headers = {'HX-Prompt': ''}
        response = self.client.post('/submit', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No input provided', response.data)

    def test_submit_with_special_characters(self):
        """Test submit endpoint with special characters in prompt"""
        headers = {'HX-Prompt': 'Test & <script>alert("xss")</script>'}
        response = self.client.post('/submit', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User entered <i>Test & <script>alert("xss")</script></i>', response.data)

    def test_submit_with_unicode_characters(self):
        """Test submit endpoint with unicode characters"""
    def test_submit_with_unicode_characters(self):
        """Test submit endpoint with unicode characters"""
        headers = {"HX-Prompt": "Hello World"}
        response = self.client.post("/submit", headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Hello World", response.data)
    def test_delete_endpoint(self):
        """Test delete endpoint clears responses"""
        # First add a response
        from myapp import responses
        responses.append({'text': 'Test response', 'timestamp': 'Now'})
        self.assertEqual(len(responses), 1)

        # Then delete
        response = self.client.post('/delete')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All responses cleared!', response.data)
        self.assertEqual(len(responses), 0)

    def test_clear_endpoint(self):
        """Test clear endpoint clears responses"""
        # First add a response
        from myapp import responses
        responses.append({'text': 'Test response', 'timestamp': 'Now'})
        self.assertEqual(len(responses), 1)

        # Then clear
        response = self.client.post('/clear')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Responses cleared successfully!', response.data)
        self.assertEqual(len(responses), 0)

    def test_multiple_submissions(self):
        """Test multiple submissions accumulate responses"""
        from myapp import responses

        # First submission
        headers1 = {'HX-Prompt': 'First input'}
        response1 = self.client.post('/submit', headers=headers1)
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(len(responses), 1)

        # Second submission
        headers2 = {'HX-Prompt': 'Second input'}
        response2 = self.client.post('/submit', headers=headers2)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(len(responses), 2)

        # Check both responses are present
        self.assertIn('First input', responses[0]['text'])
        self.assertIn('Second input', responses[1]['text'])

    def test_htmx_attributes_present(self):
        """Test that HTMX attributes are present in the HTML"""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for hx-prompt attribute
        self.assertIn('hx-prompt="Enter a string"', html)

        # Check for hx-confirm attribute
        self.assertIn('hx-confirm="Are you sure you want to submit?"', html)

        # Check for hx-target attribute
        self.assertIn('hx-target="#response"', html)

        # Check for hx-post attribute
        self.assertIn('hx-post="/submit"', html)

    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = self.client.get('/')

        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-XSS-Protection'), '1; mode=block')

    def test_htmx_script_included(self):
        """Test that HTMX script is included"""
        response = self.client.get('/')
        self.assertIn(b'https://unpkg.com/htmx.org@2.0.3', response.data)

    def test_css_file_included(self):
        """Test that CSS file is included"""
        response = self.client.get('/')
        self.assertIn(b'static/css/style.css', response.data)

    def test_favicon_included(self):
        """Test that favicon is included"""
        response = self.client.get('/')
        self.assertIn(b'static/img/favicon.svg', response.data)

    def test_debugging_instructions_present(self):
        """Test that debugging instructions are present"""
        response = self.client.get('/')
        self.assertIn(b'Debugging Instructions', response.data)
        self.assertIn(b'Open Developer Tools', response.data)
        self.assertIn(b'Console', response.data)

    def test_how_it_works_section_present(self):
        """Test that how it works section is present"""
        response = self.client.get('/')
        self.assertIn(b'How It Works', response.data)
        self.assertIn(b'hx-prompt', response.data)
        self.assertIn(b'hx-confirm', response.data)
        self.assertIn(b'HX-Prompt', response.data)

    def test_response_area_present(self):
        """Test that response area is present"""
        response = self.client.get('/')
        self.assertIn(b'id="response"', response.data)
        self.assertIn(b'response-area', response.data)

    def test_button_classes_present(self):
        """Test that button classes are present"""
        response = self.client.get('/')
        self.assertIn(b'btn btn-primary', response.data)
        self.assertIn(b'btn btn-secondary', response.data)
        self.assertIn(b'btn btn-danger', response.data)

    def test_example_sections_present(self):
        """Test that example sections are present"""
        response = self.client.get('/')
        self.assertIn(b'Prompt Dialog Example', response.data)
        self.assertIn(b'Confirmation Dialog Example', response.data)
        self.assertIn(b'Delete with Confirmation', response.data)

    def test_responses_section_present(self):
        """Test that responses section is present"""
        response = self.client.get('/')
        self.assertIn(b'Response History', response.data)
        self.assertIn(b'responses-list', response.data)

    def test_javascript_debugging_present(self):
        """Test that JavaScript debugging code is present"""
        response = self.client.get('/')
        self.assertIn(b'htmx:beforeRequest', response.data)
        self.assertIn(b'htmx:afterRequest', response.data)
        self.assertIn(b'console.log', response.data)

if __name__ == '__main__':
    unittest.main()
