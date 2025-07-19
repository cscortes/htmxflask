#!/usr/bin/env python3
"""
Unit tests for HTMX Progress Bar Example

This test file verifies the server-side logic works correctly,
helping isolate whether issues are server-side or client-side.
Based on the official HTMX progress bar example implementation.
"""

import unittest
from myapp import app
import myapp


class TestProgressBar(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        # Reset progress for each test
        myapp.PROGRESS = 0

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('Progress Bar', html)
        self.assertIn('Start server side task', html)
        self.assertIn('hx-post="/job/start"', html)

    def test_start_endpoint_returns_progress_html(self):
        """Test that /job/start returns progress bar HTML."""
        response = self.client.post('/job/start')
        self.assertEqual(response.status_code, 200)

        # Check that response contains progress bar HTML
        html = response.get_data(as_text=True)
        self.assertIn('Running', html)
        self.assertIn('hx-get="/job/progress"', html)
        self.assertIn('hx-trigger="every 600ms"', html)
        self.assertIn('hx-target="this"', html)
        self.assertIn('hx-swap="innerHTML"', html)
        self.assertIn('progress', html)
        self.assertIn('progress-bar', html)
        self.assertIn('width:0%', html)
        self.assertIn('aria-valuenow="0"', html)

    def test_job_progress_endpoint_increments(self):
        """Test that /job/progress increments progress."""
        # Reset progress to ensure clean state
        myapp.PROGRESS = 0

        response = self.client.get('/job/progress')
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('progress', html)
        self.assertIn('progress-bar', html)
        # Check for 5% increment (first call after reset)
        self.assertIn('width:5%', html)
        self.assertIn('aria-valuenow="5"', html)

    def test_job_progress_completion(self):
        """Test that /job/progress handles completion at 100%."""
        # Set progress to 95 (next increment will be 100)
        myapp.PROGRESS = 95

        response = self.client.get('/job/progress')
        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)
        self.assertIn('width:100%', html)
        self.assertIn('aria-valuenow="100"', html)

    def test_progress_increments_correctly(self):
        """Test that progress increments correctly over multiple calls."""
        # Reset progress to ensure clean state
        myapp.PROGRESS = 0

        # Test multiple progress updates (5% increments)
        expected_progresses = [5, 10, 15, 20, 25]
        for i, expected_progress in enumerate(expected_progresses):
            response = self.client.get('/job/progress')
            self.assertEqual(response.status_code, 200)

            html = response.get_data(as_text=True)
            self.assertIn(f'width:{expected_progress}%', html)
            self.assertIn(f'aria-valuenow="{expected_progress}"', html)

    def test_html_structure_validation(self):
        """Test that HTML structure matches official HTMX example."""
        # Test start endpoint HTML structure
        response = self.client.post('/job/start')
        html = response.get_data(as_text=True)

        # Check for proper HTML structure (more flexible matching)
        self.assertIn('hx-trigger="done"', html)
        self.assertIn('hx-get="/job/done"', html)
        self.assertIn('hx-swap="outerHTML"', html)
        self.assertIn('hx-target="this"', html)
        self.assertIn('role="status"', html)
        self.assertIn('id="pblabel"', html)
        self.assertIn('Running', html)
        self.assertIn('hx-get="/job/progress"', html)
        self.assertIn('hx-trigger="every 600ms"', html)
        self.assertIn('class="progress"', html)
        self.assertIn('role="progressbar"', html)
        self.assertIn('aria-valuemin="0"', html)
        self.assertIn('aria-valuemax="100"', html)
        self.assertIn('aria-valuenow="0"', html)
        self.assertIn('class="progress-bar"', html)
        self.assertIn('width:0%', html)

    def test_css_class_names(self):
        """Test that proper CSS class names are used."""
        response = self.client.post('/job/start')
        html = response.get_data(as_text=True)

        # Check for Bootstrap-style CSS classes
        self.assertIn('class="progress"', html)
        self.assertIn('class="progress-bar"', html)

    def test_debug_output(self):
        """Test that prints actual HTML output for debugging."""
        # Test start endpoint
        start_response = self.client.post('/job/start')
        self.assertEqual(start_response.status_code, 200)
        start_html = start_response.get_data(as_text=True)

        print("\n=== START ENDPOINT HTML OUTPUT ===")
        print(start_html)
        print("=== END START HTML ===\n")

        # Test progress endpoint
        # Reset progress to ensure clean state
        myapp.PROGRESS = 0

        progress_response = self.client.get('/job/progress')
        self.assertEqual(progress_response.status_code, 200)
        progress_html = progress_response.get_data(as_text=True)

        print("=== PROGRESS ENDPOINT HTML OUTPUT ===")
        print(progress_html)
        print("=== END PROGRESS HTML ===\n")


if __name__ == '__main__':
    unittest.main(verbosity=2)