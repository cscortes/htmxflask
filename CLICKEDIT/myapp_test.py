#!/usr/bin/env python3
"""
Unit tests for HTMX Click-to-Edit Example

This test file verifies the server-side logic works correctly,
helping isolate whether issues are server-side or client-side.
Based on the official HTMX click-to-edit example implementation.
"""

import unittest
from myapp import app


class TestClickToEdit(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Reset contact data to original state
        import myapp
        myapp.CONTACT.clear()
        myapp.CONTACT.update({
            "firstName": "Manny",
            "lastName": "Pacquiao",
            "email": "manny@pacquiao.com"
        })

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('HTMX Click-to-Edit Example', html)
        self.assertIn('Manny', html)
        self.assertIn('Pacquiao', html)
        self.assertIn('manny@pacquiao.com', html)
        self.assertIn('Click To Edit', html)

    def test_contact_display_structure(self):
        """Test that contact display has proper structure."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for contact information
        self.assertIn('First Name', html)
        self.assertIn('Last Name', html)
        self.assertIn('Email', html)
        self.assertIn('Manny', html)
        self.assertIn('Pacquiao', html)
        self.assertIn('manny@pacquiao.com', html)

        # Check for HTMX attributes
        self.assertIn('hx-target="this"', html)
        self.assertIn('hx-swap="outerHTML"', html)
        self.assertIn('hx-get="/contact/edit"', html)

    def test_edit_form_loads(self):
        """Test that edit form loads correctly."""
        response = self.client.get('/contact/edit')
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('Manny', html)
        self.assertIn('Pacquiao', html)
        self.assertIn('manny@pacquiao.com', html)
        self.assertIn('Submit', html)
        self.assertIn('Cancel', html)
        self.assertIn('hx-put="/contact/update"', html)

    def test_edit_form_structure(self):
        """Test that edit form has proper HTML structure."""
        response = self.client.get('/contact/edit')
        html = response.get_data(as_text=True)

        # Check for form elements
        self.assertIn('<form', html)
        self.assertIn('hx-put="/contact/update"', html)
        self.assertIn('hx-target="this"', html)
        self.assertIn('hx-swap="outerHTML"', html)
        self.assertIn('<input type="text" name="firstName"', html)
        self.assertIn('<input type="text" name="lastName"', html)
        self.assertIn('<input type="email" name="email"', html)

    def test_contact_update(self):
        """Test that contact information can be updated."""
        # Update contact data
        data = {
            'firstName': 'Jane',
            'lastName': 'Doe',
            'email': 'jane@doe.com'
        }

        response = self.client.put('/contact/update', data=data)
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('Jane', html)
        self.assertIn('Doe', html)
        self.assertIn('jane@doe.com', html)

    def test_contact_cancel(self):
        """Test that cancel returns to display view."""
        response = self.client.get('/contact/cancel')
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('Manny', html)
        self.assertIn('Pacquiao', html)
        self.assertIn('manny@pacquiao.com', html)
        self.assertIn('Click To Edit', html)

    def test_html_structure_validation(self):
        """Test that HTML structure matches expected patterns."""
        # Test main page structure
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for proper HTMX attributes
        self.assertIn('hx-get="/contact/edit"', html)
        self.assertIn('hx-target="this"', html)
        self.assertIn('hx-swap="outerHTML"', html)

        # Test edit form structure
        response = self.client.get('/contact/edit')
        html = response.get_data(as_text=True)

        # Check for form structure
        self.assertIn('hx-put="/contact/update"', html)
        self.assertIn('name="firstName"', html)
        self.assertIn('name="lastName"', html)
        self.assertIn('name="email"', html)

    def test_css_class_names(self):
        """Test that proper CSS class names are used."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for CSS classes
        self.assertIn('class="btn primary"', html)
        self.assertIn('class="container"', html)

    def test_debug_output(self):
        """Test that prints actual HTML output for debugging."""
        # Test main page
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        print("\n=== MAIN PAGE HTML OUTPUT ===")
        print(html[:500] + "..." if len(html) > 500 else html)
        print("=== END MAIN PAGE HTML ===\n")

        # Test edit form
        response = self.client.get('/contact/edit')
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)

        print("=== EDIT FORM HTML OUTPUT ===")
        print(html)
        print("=== END EDIT FORM HTML ===\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)
