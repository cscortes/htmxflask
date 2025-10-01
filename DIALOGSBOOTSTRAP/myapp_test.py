#!/usr/bin/env python3

import unittest
from myapp import app

class TestDialogsBootstrapExample(unittest.TestCase):
    """Test cases for the DIALOGSBOOTSTRAP example"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page_loads(self):
        """Test that the main page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HTMX Bootstrap Modal Dialogs', response.data)

    def test_index_contains_htmx_attributes(self):
        """Test that the page contains required HTMX attributes"""
        response = self.app.get('/')
        self.assertIn(b'hx-get="/modal"', response.data)
        self.assertIn(b'hx-target="#modals-here .modal-content"', response.data)
        self.assertIn(b'hx-trigger="click"', response.data)

    def test_index_contains_bootstrap_attributes(self):
        """Test that the page contains Bootstrap modal attributes"""
        response = self.app.get('/')
        self.assertIn(b'data-bs-toggle="modal"', response.data)
        self.assertIn(b'data-bs-target="#modals-here"', response.data)
        self.assertIn(b'class="modal modal-blur fade"', response.data)

    def test_modal_endpoint_loads(self):
        """Test that the modal endpoint returns modal content"""
        response = self.app.get('/modal')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<div class="modal-header">', response.data)
        self.assertIn(b'<h5 class="modal-title">', response.data)
        self.assertIn(b'Bootstrap Modal Dialog</h5>', response.data)

    def test_modal_contains_bootstrap_structure(self):
        """Test that modal contains proper Bootstrap modal structure"""
        response = self.app.get('/modal')
        self.assertIn(b'<div class="modal-header">', response.data)
        self.assertIn(b'<div class="modal-body">', response.data)
        self.assertIn(b'<div class="modal-footer">', response.data)

    def test_modal_contains_close_button(self):
        """Test that modal contains Bootstrap close button"""
        response = self.app.get('/modal')
        self.assertIn(b'data-bs-dismiss="modal"', response.data)
        self.assertIn(b'class="btn-close"', response.data)
        self.assertIn(b'aria-label="Close"', response.data)

    def test_modal_contains_footer_buttons(self):
        """Test that modal footer contains close button"""
        response = self.app.get('/modal')
        self.assertIn(b'<button type="button" class="btn btn-secondary"', response.data)
        self.assertIn(b'data-bs-dismiss="modal"', response.data)

    def test_index_contains_how_it_works_section(self):
        """Test that the page contains educational content"""
        response = self.app.get('/')
        self.assertIn(b'How It Works', response.data)
        self.assertIn(b'hx-get="/modal"', response.data)
        self.assertIn(b'data-bs-toggle="modal"', response.data)

    def test_index_contains_bootstrap_css_link(self):
        """Test that Bootstrap CSS is included"""
        response = self.app.get('/')
        self.assertIn(b'bootstrap@5.3.0/dist/css/bootstrap.min.css', response.data)

    def test_index_contains_bootstrap_js_link(self):
        """Test that Bootstrap JS is included"""
        response = self.app.get('/')
        self.assertIn(b'bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js', response.data)

    def test_index_contains_htmx_script(self):
        """Test that HTMX script is included"""
        response = self.app.get('/')
        self.assertIn(b'htmx.org@1.9.10', response.data)

    def test_modal_container_has_correct_id(self):
        """Test that modal container has correct ID for targeting"""
        response = self.app.get('/')
        self.assertIn(b'id="modals-here"', response.data)

    def test_modal_container_has_bootstrap_classes(self):
        """Test that modal container has proper Bootstrap classes"""
        response = self.app.get('/')
        self.assertIn(b'class="modal modal-blur fade"', response.data)
        self.assertIn(b'class="modal-dialog modal-lg modal-dialog-centered"', response.data)

    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = self.app.get('/')
        self.assertIn('Content-Security-Policy', response.headers)
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)

    def test_modal_content_contains_alert(self):
        """Test that modal contains informational alert"""
        response = self.app.get('/modal')
        self.assertIn(b'<div class="alert alert-info">', response.data)
        self.assertIn(b'Key Features:', response.data)

    def test_modal_content_contains_code_examples(self):
        """Test that modal contains code examples"""
        response = self.app.get('/modal')
        self.assertIn(b'<code>hx-get="/modal"</code>', response.data)

    def test_index_contains_htmx_patterns_section(self):
        """Test that index page explains HTMX patterns"""
        response = self.app.get('/')
        self.assertIn(b'HTMX Patterns Used:', response.data)
        self.assertIn(b'hx-get', response.data)
        self.assertIn(b'hx-target', response.data)
        self.assertIn(b'hx-trigger="click"', response.data)

    def test_index_contains_bootstrap_features_section(self):
        """Test that index page explains Bootstrap features"""
        response = self.app.get('/')
        self.assertIn(b'Bootstrap Features:', response.data)
        self.assertIn(b'data-bs-toggle="modal"', response.data)
        self.assertIn(b'modal-lg modal-dialog-centered', response.data)

    def test_modal_dialog_has_proper_attributes(self):
        """Test that modal dialog has proper accessibility attributes"""
        response = self.app.get('/')
        self.assertIn(b'role="document"', response.data)
        self.assertIn(b'aria-hidden="true"', response.data)
        self.assertIn(b'tabindex="-1"', response.data)

if __name__ == '__main__':
    unittest.main()
