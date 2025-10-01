#!/usr/bin/env python3

import unittest
from myapp import app


class TestDialogsCustomExample(unittest.TestCase):
    """Test cases for the DIALOGSCUSTOM example"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page_loads(self):
        """Test that the main page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HTMX Custom Modal Dialogs', response.data)

    def test_index_contains_htmx_attributes(self):
        """Test that the page contains required HTMX attributes"""
        response = self.app.get('/')
        self.assertIn(b'hx-get="/modal"', response.data)
        self.assertIn(b'hx-target="body"', response.data)
        self.assertIn(b'hx-swap="beforeend"', response.data)

    def test_index_contains_hyperscript(self):
        """Test that Hyperscript is loaded"""
        response = self.app.get('/')
        self.assertIn(b'hyperscript.org', response.data)

    def test_modal_endpoint_loads(self):
        """Test that the modal endpoint returns modal content"""
        response = self.app.get('/modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<div id="modal"', response.data)
        self.assertIn(b'Modal Dialog', response.data)

    def test_modal_contains_hyperscript_close_handler(self):
        """Test that modal contains Hyperscript close handler"""
        response = self.app.get('/modal')
        self.assertIn(b'on closeModal', response.data)
        self.assertIn(b'add .closing', response.data)
        self.assertIn(b'wait for animationend', response.data)
        self.assertIn(b'remove me', response.data)

    def test_modal_contains_underlay(self):
        """Test that modal contains underlay with click handler"""
        response = self.app.get('/modal')
        self.assertIn(b'class="modal-underlay"', response.data)
        self.assertIn(b'on click trigger closeModal', response.data)

    def test_modal_contains_close_button(self):
        """Test that modal contains close button"""
        response = self.app.get('/modal')
        self.assertIn(b'class="btn danger"', response.data)
        self.assertIn(b'trigger closeModal', response.data)

    def test_modal_contains_content_section(self):
        """Test that modal contains modal-content div"""
        response = self.app.get('/modal')
        self.assertIn(b'class="modal-content"', response.data)

    def test_index_contains_how_it_works_section(self):
        """Test that the page contains educational content"""
        response = self.app.get('/')
        self.assertIn(b'How It Works', response.data)
        self.assertIn(b'hx-swap="beforeend"', response.data)

    def test_index_contains_htmx_script(self):
        """Test that HTMX script is included"""
        response = self.app.get('/')
        self.assertIn(b'htmx.org@1.9.10', response.data)

    def test_index_contains_hyperscript_script(self):
        """Test that Hyperscript script is included"""
        response = self.app.get('/')
        self.assertIn(b'hyperscript.org@0.9.12', response.data)

    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = self.app.get('/')
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)

    def test_modal_info_section(self):
        """Test that modal contains informational section"""
        response = self.app.get('/modal')
        self.assertIn(b'class="modal-info"', response.data)
        self.assertIn(b'How This Works:', response.data)

    def test_index_htmx_patterns_section(self):
        """Test that index explains HTMX patterns"""
        response = self.app.get('/')
        self.assertIn(b'HTMX Patterns Used:', response.data)
        self.assertIn(b'hx-get', response.data)
        self.assertIn(b'hx-target="body"', response.data)

    def test_index_hyperscript_features_section(self):
        """Test that index explains Hyperscript features"""
        response = self.app.get('/')
        self.assertIn(b'Hyperscript Features:', response.data)
        self.assertIn(b'closeModal', response.data)

    def test_index_key_features_section(self):
        """Test that index lists key features"""
        response = self.app.get('/')
        self.assertIn(b'Key Features:', response.data)
        self.assertIn(b'No CSS framework dependencies', response.data)

    def test_modal_contains_descriptive_text(self):
        """Test that modal contains descriptive content"""
        response = self.app.get('/modal')
        self.assertIn(b'loaded dynamically from the server', response.data)

    def test_csp_allows_hyperscript(self):
        """Test that CSP allows Hyperscript and HTMX"""
        response = self.app.get('/')
        csp = response.headers.get('Content-Security-Policy')
        self.assertIn('https://unpkg.com', csp)

    def test_index_contains_demo_button(self):
        """Test that index contains demo button"""
        response = self.app.get('/')
        self.assertIn(b'class="btn primary"', response.data)
        self.assertIn(b'Open a Modal', response.data)

    def test_modal_hyperscript_syntax(self):
        """Test that modal uses correct Hyperscript syntax"""
        response = self.app.get('/modal')
        self.assertIn(b'_="on closeModal add .closing then wait for animationend then remove me"', response.data)


if __name__ == '__main__':
    unittest.main()

