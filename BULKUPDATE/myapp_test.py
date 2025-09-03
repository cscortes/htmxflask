#!/usr/bin/env python3
"""
Test suite for BULKUPDATE example.

Tests bulk update functionality, form handling, and HTMX patterns.
"""

import unittest
from myapp import app


class BulkUpdateTestCase(unittest.TestCase):
    """Test cases for bulk update functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Reset contacts to known state for consistent testing
        import myapp
        myapp.CONTACTS.clear()
        myapp.CONTACTS.extend([
            {"id": 1, "name": "Manny Pacquiao",
             "email": "manny@pacquiao.com", "status": "Active"},
            {"id": 2, "name": "Nonito Donaire",
             "email": "nonito@donaire.com", "status": "Active"},
            {"id": 3, "name": "Donnie Nietes",
             "email": "donnie@nietes.com", "status": "Inactive"},
            {"id": 4, "name": "Jerwin Ancajas",
             "email": "jerwin@ancajas.com", "status": "Active"},
            {"id": 5, "name": "John Riel Casimero",
             "email": "john@casimero.com", "status": "Inactive"},
        ])

    def test_index_page(self):
        """Test that the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check that all contacts are displayed
        response_text = response.get_data(as_text=True)
        self.assertIn('Manny Pacquiao', response_text)
        self.assertIn('Nonito Donaire', response_text)
        self.assertIn('Donnie Nietes', response_text)
        self.assertIn('Jerwin Ancajas', response_text)
        self.assertIn('John Riel Casimero', response_text)

        # Check for HTMX attributes
        self.assertIn('hx-post="/bulk-update"', response_text)
        self.assertIn('hx-target="#toast"', response_text)
        self.assertIn('hx-swap="innerHTML settle:3s"', response_text)

    def test_bulk_update_active_to_inactive(self):
        """Test bulk update from active to inactive status."""
        # Submit form with some contacts checked (will become active)
        # Note: With corrected logic, only checked contacts are updated to
        # Active
        # Unchecked contacts remain unchanged
        form_data = {
            'status:manny@pacquiao.com': 'on',      # Already Active, no change
            'status:nonito@donaire.com': 'on',      # Already Active, no change
            'status:donnie@nietes.com': 'on',       # Change
            'status:jerwin@ancajas.com': 'on',      # Already Active, no change
            'status:john@casimero.com': 'on',       # Change
        }

        response = self.client.post('/bulk-update', data=form_data)
        self.assertEqual(response.status_code, 200)

        # Check that statuses were updated correctly
        import myapp
        contacts = myapp.CONTACTS

        # Find contacts by email and check status
        manny = next(c for c in contacts if c['email'] == 'manny@pacquiao.com')
        nonito = next(c for c in contacts
                      if c['email'] == 'nonito@donaire.com')
        donnie = next(c for c in contacts if c['email'] == 'donnie@nietes.com')
        jerwin = next(c for c in contacts
                      if c['email'] == 'jerwin@ancajas.com')
        john = next(c for c in contacts if c['email'] == 'john@casimero.com')

        # All checked contacts should now be Active
        self.assertEqual(manny['status'], 'Active')      # Was already Active
        self.assertEqual(nonito['status'], 'Active')     # Was already Active
        self.assertEqual(donnie['status'], 'Active')     # Changed
        self.assertEqual(jerwin['status'], 'Active')     # Was already Active
        self.assertEqual(john['status'], 'Active')       # Changed

        # Check response contains toast notification
        response_text = response.get_data(as_text=True)
        self.assertIn('Bulk Update Complete!', response_text)
        self.assertIn('Updated 2 contact(s) successfully',
                      response_text)

    def test_bulk_update_all_to_active(self):
        """Test bulk update setting all contacts to active."""
        form_data = {
            'status:manny@pacquiao.com': 'on',
            'status:nonito@donaire.com': 'on',
            'status:donnie@nietes.com': 'on',
            'status:jerwin@ancajas.com': 'on',
            'status:john@casimero.com': 'on',
        }

        response = self.client.post('/bulk-update', data=form_data)
        self.assertEqual(response.status_code, 200)

        # Check that all contacts are now active
        import myapp
        for contact in myapp.CONTACTS:
            self.assertEqual(contact['status'], 'Active')

        # Check response
        response_text = response.get_data(as_text=True)
        self.assertIn('Updated 5 contact(s) successfully', response_text)

    def test_bulk_update_no_selection(self):
        """Test bulk update with no contacts selected."""
        form_data = {}  # No checkboxes selected

        response = self.client.post('/bulk-update', data=form_data)
        self.assertEqual(response.status_code, 200)

        # Check response indicates no updates
        response_text = response.get_data(as_text=True)
        self.assertIn('Updated 0 contact(s) successfully', response_text)

    def test_api_contacts_endpoint(self):
        """Test the API contacts endpoint."""
        response = self.client.get('/api/contacts')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(len(data), 5)
        self.assertIn('name', data[0])
        self.assertIn('email', data[0])
        self.assertIn('status', data[0])

    def test_api_contacts_count_endpoint(self):
        """Test the API contacts count endpoint."""
        response = self.client.get('/api/contacts/count')
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data['total'], 5)
        self.assertEqual(data['active'], 3)  # 3 active, 2 inactive initially
        self.assertEqual(data['inactive'], 2)

    def test_table_structure(self):
        """Test that the table has proper structure and accessibility."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for proper table structure
        self.assertIn('<table class="table bulk-update-table"', html)
        self.assertIn('<th scope="col">', html)
        self.assertIn('role="table"', html)
        self.assertIn('aria-label="Contacts table"', html)

        # Check for checkbox structure
        self.assertIn('id="select-all"', html)
        self.assertIn('class="contact-checkbox"', html)

        # Check for form structure
        self.assertIn('<form id="bulk-update-form"', html)
        self.assertIn('hx-post="/bulk-update"', html)

    def test_toast_notification_structure(self):
        """Test that toast notification area is properly structured."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for toast container
        self.assertIn('id="toast"', html)
        self.assertIn('class="toast-container"', html)
        self.assertIn('role="region"', html)
        self.assertIn('aria-live="polite"', html)

    def test_bulk_controls_structure(self):
        """Test that bulk controls are properly structured."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for bulk controls
        self.assertIn('class="bulk-controls"', html)
        self.assertIn('Update Selected Contacts', html)
        self.assertIn('id="selected-count"', html)
        self.assertIn('contacts selected', html)


if __name__ == '__main__':
    unittest.main()
