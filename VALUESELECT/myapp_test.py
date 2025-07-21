#!/usr/bin/env python3
"""
Unit tests for VALUESELECT example.

Tests the cascading dropdown functionality with HTMX patterns:
- hx-get: Load model options for selected make
- hx-target: Update model dropdown
- hx-trigger: Change event on make dropdown
"""

import unittest
import tempfile
import os
import shutil
from myapp import app, mmdb, load_car_data


class TestValueSelect(unittest.TestCase):
    """Test suite for VALUESELECT functionality."""

    def setUp(self):
        """Set up test client and sample data."""
        self.app = app.test_client()
        self.app.testing = True

        # Create a temporary CSV file for testing
        self.temp_csv = tempfile.NamedTemporaryFile(
            mode='w', suffix='.csv', delete=False)
        self.temp_csv.write("'Toyota','RAV4'\n")
        self.temp_csv.write("'Toyota','Highlander'\n")
        self.temp_csv.write("'Honda','CR-V'\n")
        self.temp_csv.write("'Honda','Pilot'\n")
        self.temp_csv.write("'Ford','Escape'\n")
        self.temp_csv.write("'Ford','Explorer'\n")
        self.temp_csv.close()

        # Store original CSV path and replace with temp file
        self.original_csv_path = "car.csv"
        if os.path.exists(self.original_csv_path):
            os.rename(self.original_csv_path, self.original_csv_path + ".bak")

        shutil.copy(self.temp_csv.name, self.original_csv_path)

        # Reload data with test CSV
        mmdb.clear()
        load_car_data()

    def tearDown(self):
        """Clean up test files."""
        # Remove test CSV
        if os.path.exists(self.original_csv_path):
            os.remove(self.original_csv_path)

        # Restore original CSV if it existed
        if os.path.exists(self.original_csv_path + ".bak"):
            os.rename(self.original_csv_path + ".bak", self.original_csv_path)

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Car Selector', response.data)

    def test_models_endpoint_exists(self):
        """Test that the models endpoint responds."""
        response = self.app.get('/models/?makeselected=Toyota')
        self.assertEqual(response.status_code, 200)

    def test_models_endpoint_with_valid_make(self):
        """Test models endpoint with valid make selection."""
        response = self.app.get('/models/?makeselected=Toyota')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Should contain Toyota models
        self.assertIn('RAV4', html)
        self.assertIn('Highlander', html)
        self.assertIn('<option', html)

    def test_models_endpoint_with_different_make(self):
        """Test models endpoint with different make selection."""
        response = self.app.get('/models/?makeselected=Honda')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Should contain Honda models
        self.assertIn('CR-V', html)
        self.assertIn('Pilot', html)
        self.assertNotIn('RAV4', html)

    def test_models_endpoint_with_invalid_make(self):
        """Test models endpoint with invalid make selection."""
        response = self.app.get('/models/?makeselected=InvalidMake')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Should return "No models available"
        self.assertIn('No models available', html)

    def test_models_endpoint_with_missing_make(self):
        """Test models endpoint with missing make parameter."""
        response = self.app.get('/models/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Should return "No models available"
        self.assertIn('No models available', html)

    def test_models_endpoint_with_empty_make(self):
        """Test models endpoint with empty make parameter."""
        response = self.app.get('/models/?makeselected=')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Should return "No models available"
        self.assertIn('No models available', html)

    def test_html_structure_validation(self):
        """Test that HTML structure matches expected patterns."""
        response = self.app.get('/models/?makeselected=Toyota')
        html = response.data.decode('utf-8')

        # Should contain option elements
        self.assertIn('<option', html)
        self.assertIn('</option>', html)
        self.assertIn('value="', html)

    def test_data_loading(self):
        """Test that car data is loaded correctly."""
        # Check that makes are loaded
        self.assertIn('Toyota', mmdb)
        self.assertIn('Honda', mmdb)
        self.assertIn('Ford', mmdb)

        # Check that models are loaded
        self.assertIn('RAV4', mmdb['Toyota'])
        self.assertIn('Highlander', mmdb['Toyota'])
        self.assertIn('CR-V', mmdb['Honda'])
        self.assertIn('Pilot', mmdb['Honda'])

    def test_index_page_has_makes(self):
        """Test that index page includes all makes."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain all makes
        self.assertIn('Toyota', html)
        self.assertIn('Honda', html)
        self.assertIn('Ford', html)

    def test_index_page_has_initial_models(self):
        """Test that index page includes initial models."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain models from first make (Ford in test data)
        self.assertIn('Escape', html)
        self.assertIn('Explorer', html)

    def test_css_class_names(self):
        """Test that proper CSS class names are used."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain expected CSS classes
        self.assertIn('class="', html)

    def test_htmx_attributes(self):
        """Test that HTMX attributes are present."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain HTMX attributes
        self.assertIn('hx-get', html)
        self.assertIn('hx-target', html)
        self.assertIn('hx-trigger', html)

    def test_debug_output(self):
        """Test that prints actual HTML output for debugging."""
        print("\n=== MAIN PAGE HTML OUTPUT ===")
        response = self.app.get('/')
        print(response.data.decode('utf-8')[:500] + "...")
        print("=== END MAIN PAGE HTML ===\n")

        print("=== MODELS ENDPOINT HTML OUTPUT ===")
        response = self.app.get('/models/?makeselected=Toyota')
        print(response.data.decode('utf-8'))
        print("=== END MODELS ENDPOINT HTML ===\n")


if __name__ == '__main__':
    unittest.main()
