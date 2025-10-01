#!/usr/bin/env python3
"""
Unit tests for RESETINPUT example.

Tests the reset user input functionality including:
- Form submission and note creation
- HTML fragment responses
- HTMX event handling
- Error handling
- Note listing and clearing
"""

import unittest
from unittest.mock import patch
import tempfile
import os
from myapp import app, notes

class TestResetInput(unittest.TestCase):
    """Test cases for the Reset Input example."""

    def setUp(self):
        """Set up test client and clear notes."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Clear notes before each test
        notes.clear()

    def tearDown(self):
        """Clean up after each test."""
        notes.clear()

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reset User Input', response.data)
        self.assertIn(b'hx-on::after-request', response.data)
        self.assertIn(b'this.reset()', response.data)

    def test_add_note_success(self):
        """Test successful note creation."""
        response = self.client.post('/note', data={'note-text': 'Test note'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test note', response.data)
        self.assertIn(b'note-item', response.data)
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0]['text'], 'Test note')

    def test_add_note_empty(self):
        """Test adding empty note returns error."""
        response = self.client.post('/note', data={'note-text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Note cannot be empty', response.data)
        self.assertEqual(len(notes), 0)

    def test_add_note_whitespace_only(self):
        """Test adding whitespace-only note returns error."""
        response = self.client.post('/note', data={'note-text': '   '})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Note cannot be empty', response.data)
        self.assertEqual(len(notes), 0)

    def test_add_multiple_notes(self):
        """Test adding multiple notes."""
        # Add first note
        response1 = self.client.post('/note', data={'note-text': 'First note'})
        self.assertEqual(response1.status_code, 200)

        # Add second note
        response2 = self.client.post('/note', data={'note-text': 'Second note'})
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(len(notes), 2)
        self.assertEqual(notes[0]['text'], 'First note')
        self.assertEqual(notes[1]['text'], 'Second note')

    def test_note_has_timestamp(self):
        """Test that notes include timestamps."""
        response = self.client.post('/note', data={'note-text': 'Timestamped note'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'note-timestamp', response.data)
        self.assertEqual(len(notes), 1)
        self.assertIn('timestamp', notes[0])

    def test_get_notes_empty(self):
        """Test getting notes when none exist."""
        response = self.client.get('/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No notes yet', response.data)

    def test_get_notes_with_content(self):
        """Test getting notes when some exist."""
        # Add a note first
        self.client.post('/note', data={'note-text': 'Test note for listing'})

        response = self.client.get('/notes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test note for listing', response.data)
        self.assertIn(b'note-item', response.data)

    def test_clear_notes(self):
        """Test clearing all notes."""
        # Add some notes first
        self.client.post('/note', data={'note-text': 'Note 1'})
        self.client.post('/note', data={'note-text': 'Note 2'})
        self.assertEqual(len(notes), 2)

        # Clear notes
        response = self.client.post('/clear')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All notes cleared', response.data)
        self.assertEqual(len(notes), 0)

    def test_html_fragment_structure(self):
        """Test that returned HTML fragments have correct structure."""
        response = self.client.post('/note', data={'note-text': 'Structure test'})
        self.assertEqual(response.status_code, 200)

        html = response.data.decode('utf-8')
        self.assertIn('<li class="note-item">', html)
        self.assertIn('<div class="note-content">Structure test</div>', html)
        self.assertIn('<div class="note-timestamp">', html)

    def test_htmx_attributes_present(self):
        """Test that HTMX attributes are present in the template."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for key HTMX attributes
        self.assertIn('hx-post="/note"', html)
        self.assertIn('hx-target="#notes"', html)
        self.assertIn('hx-swap="afterbegin"', html)
        self.assertIn('hx-on::after-request', html)
        self.assertIn('this.reset()', html)
        self.assertIn('hx-include="#note-input"', html)

    def test_form_methods_both_present(self):
        """Test that both form reset methods are demonstrated."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for both methods
        self.assertIn('Method 1: Form Reset', html)
        self.assertIn('Method 2: Individual Input Reset', html)
        self.assertIn('this.reset()', html)
        self.assertIn('document.getElementById', html)

    def test_security_headers(self):
        """Test that security headers are present."""
        response = self.client.get('/')
        self.assertIn('X-Content-Type-Options', response.headers)
        self.assertIn('X-Frame-Options', response.headers)
        self.assertIn('X-XSS-Protection', response.headers)

    def test_note_id_increments(self):
        """Test that note IDs increment correctly."""
        # Add first note
        self.client.post('/note', data={'note-text': 'Note 1'})
        self.assertEqual(notes[0]['id'], 1)

        # Add second note
        self.client.post('/note', data={'note-text': 'Note 2'})
        self.assertEqual(notes[1]['id'], 2)

    def test_clear_button_has_confirmation(self):
        """Test that clear button has confirmation dialog."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')
        self.assertIn('hx-confirm="Are you sure', html)

    def test_how_it_works_section(self):
        """Test that the how-it-works section is present."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('How It Works', html)
        self.assertIn('hx-on::after-request', html)
        self.assertIn('event.detail.successful', html)
        self.assertIn('this.reset()', html)
        self.assertIn('hx-swap="afterbegin"', html)
        self.assertIn('hx-include', html)

    def test_tip_section_present(self):
        """Test that the tip section about reset() method is present."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('Tip:', html)
        self.assertIn('reset()</code> method is only available on form elements', html)

    def test_htmx_configuration(self):
        """Test that HTMX configuration is present."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('htmx.config.historyEnabled = false', html)
        self.assertIn('htmx.config.allowEval = false', html)
        self.assertIn('htmx.config.allowScriptTags = false', html)

    def test_console_logging_present(self):
        """Test that console logging for debugging is present."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('htmx:afterRequest', html)
        self.assertIn('console.log', html)
        self.assertIn('evt.detail.successful', html)

    def test_form_reset_instructions_present(self):
        """Test that form reset instructions are present."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('Type a note and click "Add" - the input will automatically clear', html)
        self.assertIn('automatically clear after successful submission', html)
        self.assertIn('Open Developer Tools', html)
        self.assertIn('Console tab', html)

    def test_successful_request_returns_200(self):
        """Test that successful note creation returns 200 status."""
        response = self.client.post('/note', data={'note-text': 'Test reset functionality'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test reset functionality', response.data)

    def test_failed_request_returns_400(self):
        """Test that empty note returns 400 status (won't trigger reset)."""
        response = self.client.post('/note', data={'note-text': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Note cannot be empty', response.data)

    def test_reset_javascript_present(self):
        """Test that reset JavaScript code is present in the template."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        # Check for both reset methods in JavaScript
        self.assertIn('evt.target.reset()', html)
        self.assertIn("document.getElementById('note-input').value = ''", html)
        self.assertIn('evt.detail.successful', html)
        self.assertIn('form-reset-method', html)
        self.assertIn('input-reset-method', html)

    def test_debugging_instructions_present(self):
        """Test that debugging instructions are present."""
        response = self.client.get('/')
        html = response.data.decode('utf-8')

        self.assertIn('Debugging Instructions', html)
        self.assertIn('Open Developer Tools', html)
        self.assertIn('Console tab', html)
        self.assertIn('Resetting form via this.reset()', html)
        self.assertIn('Resetting input via getElementById', html)

if __name__ == '__main__':
    unittest.main()
