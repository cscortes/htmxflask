#!/usr/bin/env python3
"""
Test suite for HTMX Click-to-Load Example

Tests pagination functionality and HTMX interactions.
"""

import unittest
from myapp import app


class TestClickToLoad(unittest.TestCase):
    """Test cases for click-to-load functionality."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'HTMX Click-to-Load Example', response.data)

    def test_initial_contacts_display(self):
        """Test that initial contacts are displayed."""
        response = self.app.get('/')
        # Check first contact is displayed
        self.assertIn(b'Manny Pacquiao', response.data)
        # Check load more button is present
        self.assertIn(b'Load More Contacts', response.data)

    def test_contacts_endpoint_first_page(self):
        """Test loading first page of contacts."""
        response = self.app.get('/contacts/?page=1')
        self.assertEqual(response.status_code, 200)
        # Should return contacts 1-3 (first page)
        self.assertIn(b'Manny Pacquiao', response.data)
        self.assertIn(b'Nonito Donaire', response.data)
        self.assertIn(b'Donnie Nietes', response.data)

    def test_contacts_endpoint_second_page(self):
        """Test loading second page of contacts."""
        response = self.app.get('/contacts/?page=2')
        self.assertEqual(response.status_code, 200)
        # Should return contacts 4-6 (second page)
        self.assertIn(b'Jerwin Ancajas', response.data)
        self.assertIn(b'John Riel Casimero', response.data)
        self.assertIn(b'Mark Magsayo', response.data)

    def test_contacts_endpoint_last_page(self):
        """Test loading last page of contacts."""
        response = self.app.get('/contacts/?page=8')
        self.assertEqual(response.status_code, 200)
        # Should return last contact and "All contacts loaded" message
        self.assertIn(b'Irish Magno', response.data)
        self.assertIn(b'All contacts loaded', response.data)

    def test_contacts_endpoint_beyond_last_page(self):
        """Test loading beyond available contacts."""
        response = self.app.get('/contacts/?page=9')
        self.assertEqual(response.status_code, 200)
        # Should return empty with "All contacts loaded" message
        self.assertIn(b'All contacts loaded', response.data)

    def test_html_structure_validation(self):
        """Test that HTML structure matches expected patterns."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Check for HTMX attributes
        self.assertIn('hx-get="/contacts/?page=', html)
        self.assertIn('hx-target="#replaceMe"', html)
        self.assertIn('hx-swap="outerHTML"', html)

        # Check for table structure
        self.assertIn('<table class="contacts-table">', html)
        self.assertIn('<thead>', html)
        self.assertIn('<tbody>', html)

    def test_css_class_names(self):
        """Test that proper CSS class names are used."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Check for CSS classes
        self.assertIn('class="contacts-table"', html)
        self.assertIn('class="btn primary"', html)
        self.assertIn('class="htmx-indicator"', html)
        self.assertIn('class="status-active"', html)

    def test_debug_output(self):
        """Test that prints actual HTML output for debugging."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        print("\n=== MAIN PAGE HTML OUTPUT ===")
        print(html[:500] + "..." if len(html) > 500 else html)
        print("=== END MAIN PAGE HTML ===\n")

        # Test contacts endpoint
        response = self.app.get('/contacts/?page=1')
        html = response.data.decode('utf-8')

        print("=== CONTACTS FRAGMENT HTML OUTPUT ===")
        print(html)
        print("=== END CONTACTS FRAGMENT HTML ===\n")


if __name__ == '__main__':
    unittest.main()
