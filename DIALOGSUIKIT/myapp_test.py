#!/usr/bin/env python3

import unittest
from myapp import app

class DialogsUIKitTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_index_loads(self):
        """Test that the index page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1 class="uk-heading-medium">HTMX UIKit Modal Dialogs Example</h1>', response.data)

    def test_modal_endpoint_loads(self):
        """Test that the modal endpoint returns modal HTML"""
        response = self.client.get('/modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<div id="modal" class="uk-modal"', response.data)
        self.assertIn(b'<h2 class="uk-modal-title">', response.data)
        self.assertIn(b'Modal Dialog</h2>', response.data)

    def test_modal_contains_form(self):
        """Test that modal contains the expected form elements"""
        response = self.client.get('/modal')
        self.assertIn(b'<form', response.data)
        self.assertIn(b'class="uk-input"', response.data)
        self.assertIn(b'placeholder="What is Your Name?"', response.data)
        self.assertIn(b'autofocus', response.data)
        self.assertIn(b'<button type="button"', response.data)

    def test_modal_contains_hyperscript(self):
        """Test that modal contains Hyperscript for animations"""
        response = self.client.get('/modal')
        self.assertIn(b'_="on submit take .uk-open from #modal"', response.data)
        self.assertIn(b'_="on click take .uk-open from #modal', response.data)


    def test_index_contains_htmx_attributes(self):
        """Test that index.html contains necessary HTMX attributes"""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for hx-get attribute
        self.assertIn('hx-get="/modal"', html)

        # Check for hx-target attribute
        self.assertIn('hx-target="#modals-here"', html)

    def test_index_contains_uikit_classes(self):
        """Test that index.html contains UIKit CSS classes"""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for UIKit classes
        self.assertIn('uk-button uk-button-primary', html)
        self.assertIn('uk-container', html)
        self.assertIn('uk-heading-medium', html)
        self.assertIn('uk-margin-large', html)

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

    def test_modal_contains_close_button(self):
        """Test that modal contains close button with proper attributes"""
        response = self.client.get('/modal')
        self.assertIn(b'id="cancelButton"', response.data)
        self.assertIn(b'type="button"', response.data)
        self.assertIn(b'uk-button uk-button-default', response.data)

    def test_index_contains_how_it_works_section(self):
        """Test that index contains educational 'How It Works' section"""
        response = self.client.get('/')
        self.assertIn(b'<h2 class="uk-heading-small">How It Works</h2>', response.data)
        self.assertIn(b'<code>GET</code> request to <code>/modal</code>', response.data)
        self.assertIn(b'Hyperscript', response.data)

if __name__ == '__main__':
    unittest.main()
