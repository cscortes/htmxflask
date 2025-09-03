#!/usr/bin/env python3
"""
Unit tests for HTMX Delete Row Example
"""

import unittest
from myapp import app


class DeleteRowTestCase(unittest.TestCase):
    """Test cases for the delete row functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Reset contacts data to original state
        import myapp
        myapp.CONTACTS.clear()
        myapp.CONTACTS.extend([
            {"id": 1, "name": "Manny Pacquiao",
             "email": "manny@pacquiao.com", "status": "Active"},
            {"id": 2, "name": "Nonito Donaire",
             "email": "nonito@donaire.com", "status": "Active"},
            {"id": 3, "name": "Donnie Nietes",
             "email": "donnie@nietes.com", "status": "Active"},
            {"id": 4, "name": "Jerwin Ancajas",
             "email": "jerwin@ancajas.com", "status": "Active"},
            {"id": 5, "name": "John Riel Casimero",
             "email": "john@casimero.com", "status": "Active"},
            {"id": 6, "name": "Mark Magsayo",
             "email": "mark@magsayo.com", "status": "Active"},
            {"id": 7, "name": "Rey Vargas",
             "email": "rey@vargas.com", "status": "Inactive"},
            {"id": 8, "name": "Emanuel Navarrete",
             "email": "emanuel@navarrete.com", "status": "Active"},
            {"id": 9, "name": "Luis Nery",
             "email": "luis@nery.com", "status": "Active"},
            {"id": 10, "name": "Brandon Figueroa",
             "email": "brandon@figueroa.com", "status": "Active"},
        ])

    def test_index_page(self):
        """Test the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('Delete Row Example', response_text)
        self.assertIn('Manny Pacquiao', response_text)
        self.assertIn('Nonito Donaire', response_text)
        self.assertIn('John Riel Casimero', response_text)

    def test_delete_contact_success(self):
        """Test successful deletion of a contact."""
        # Verify contact exists before deletion
        response = self.client.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('Manny Pacquiao', response_text)

        # Delete contact with ID 1
        response = self.client.delete('/contact/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(), b'')

        # Verify contact is removed
        response = self.client.get('/')
        response_text = response.get_data(as_text=True)
        self.assertNotIn('Manny Pacquiao', response_text)
        self.assertIn('Nonito Donaire', response_text)
        # Other contacts remain

    def test_delete_contact_not_found(self):
        """Test deletion of non-existent contact."""
        # Try to delete contact with ID 999
        response = self.client.delete('/contact/999')
        self.assertEqual(response.status_code, 404)  # Not Found
        self.assertEqual(response.get_data(), b'Contact not found')

        # Verify all contacts still exist
        response = self.client.get('/')
        response_text = response.get_data(as_text=True)
        self.assertIn('Manny Pacquiao', response_text)
        self.assertIn('Nonito Donaire', response_text)
        self.assertIn('John Riel Casimero', response_text)

    def test_delete_multiple_contacts(self):
        """Test deleting multiple contacts in sequence."""
        # Delete first contact
        response = self.client.delete('/contact/1')
        self.assertEqual(response.status_code, 200)

        # Delete second contact
        response = self.client.delete('/contact/2')
        self.assertEqual(response.status_code, 200)

        # Verify only third contact remains
        response = self.client.get('/')
        response_text = response.get_data(as_text=True)
        self.assertNotIn('Manny Pacquiao', response_text)
        self.assertNotIn('Nonito Donaire', response_text)
        self.assertIn('John Riel Casimero', response_text)

    def test_delete_contact_with_get_method(self):
        """Test that GET method is not allowed for deletion."""
        response = self.client.get('/contact/1')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_delete_contact_with_post_method(self):
        """Test that POST method is not allowed for deletion."""
        response = self.client.post('/contact/1')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_delete_contact_with_put_method(self):
        """Test that PUT method is not allowed for deletion."""
        response = self.client.put('/contact/1')
        self.assertEqual(response.status_code, 405)  # Method Not Allowed

    def test_htmx_attributes_present(self):
        """Test that HTMX attributes are present in the HTML."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for HTMX attributes
        self.assertIn('hx-confirm="Are you sure?"', html)
        self.assertIn('hx-target="closest tr"', html)
        self.assertIn('hx-swap="outerHTML swap:1s"', html)
        self.assertIn('hx-delete="/contact/1"', html)
        self.assertIn('hx-delete="/contact/2"', html)
        self.assertIn('hx-delete="/contact/5"', html)

    def test_table_structure(self):
        """Test that the table has the correct structure."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for table headers with scope attributes
        self.assertIn('<th scope="col">ID</th>', html)
        self.assertIn('<th scope="col">Name</th>', html)
        self.assertIn('<th scope="col">Email</th>', html)
        self.assertIn('<th scope="col">Status</th>', html)
        self.assertIn('<th scope="col">Actions</th>', html)  # Action column

    def test_contact_data_display(self):
        """Test that contact data is displayed correctly."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for contact information
        self.assertIn('Manny Pacquiao', html)
        self.assertIn('manny@pacquiao.com', html)
        self.assertIn('Active', html)
        self.assertIn('Nonito Donaire', html)
        self.assertIn('nonito@donaire.com', html)


if __name__ == '__main__':
    unittest.main()
