#!/usr/bin/env python3
"""
Unit tests for PLY3 example.

Tests the three interdependent dropdowns with HTMX patterns:
- hx-post: Send dropdown change requests
- hx-target: Update all dropdowns
- hx-trigger: Change event on dropdowns
"""

import unittest
from myapp import app, get_selected_states


class TestPly3(unittest.TestCase):
    """Test suite for PLY3 functionality."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Interdependent Dropdowns', response.data)

    def test_callback_endpoint_exists(self):
        """Test that the callback endpoint responds."""
        response = self.app.post('/callback/1', data={'pos1': '1'})
        self.assertEqual(response.status_code, 200)

    def test_callback_with_selectnum_1(self):
        """Test callback when dropdown 1 is changed."""
        response = self.app.post('/callback/1', data={'pos1': '2'})
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Should contain all three dropdowns
        self.assertIn('pos1', html)
        self.assertIn('pos2', html)
        self.assertIn('pos3', html)

        # Dropdown 1 should have value 2 selected
        self.assertIn('value="2" selected', html)

    def test_callback_with_selectnum_2(self):
        """Test callback when dropdown 2 is changed."""
        response = self.app.post('/callback/2', data={'pos2': '3'})
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Dropdown 2 should have value 3 selected
        self.assertIn('value="3" selected', html)

    def test_callback_with_selectnum_3(self):
        """Test callback when dropdown 3 is changed."""
        response = self.app.post('/callback/3', data={'pos3': '1'})
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')

        # Dropdown 3 should have value 1 selected
        self.assertIn('value="1" selected', html)

    def test_mutual_exclusion(self):
        """Test that only one dropdown can have a non-zero value."""
        response = self.app.post('/callback/1', data={'pos1': '2'})
        html = response.data.decode('utf-8')

        # Only dropdown 1 should have a selected value
        self.assertIn('value="2" selected', html)
        self.assertIn('value="0" selected', html)  # Others should be 0

    def test_html_structure_validation(self):
        """Test that HTML structure matches expected patterns."""
        response = self.app.post('/callback/1', data={'pos1': '1'})
        html = response.data.decode('utf-8')

        # Should contain select elements
        self.assertIn('<select', html)
        self.assertIn('</select>', html)
        self.assertIn('<option', html)
        self.assertIn('</option>', html)

    def test_get_selected_states_function(self):
        """Test the get_selected_states helper function."""
        # Test with valid values
        states = get_selected_states('1')
        self.assertEqual(states, ['', 'selected', '', ''])

        states = get_selected_states('2')
        self.assertEqual(states, ['', '', 'selected', ''])

        states = get_selected_states('3')
        self.assertEqual(states, ['', '', '', 'selected'])

        states = get_selected_states('0')
        self.assertEqual(states, ['selected', '', '', ''])

    def test_get_selected_states_with_none(self):
        """Test get_selected_states with None input."""
        states = get_selected_states(None)
        self.assertEqual(states, ['selected', '', '', ''])

    def test_get_selected_states_with_invalid_values(self):
        """Test get_selected_states with invalid inputs."""
        # Test with string that can't be converted to int
        states = get_selected_states('invalid')
        self.assertEqual(states, ['selected', '', '', ''])

        # Test with out-of-range values
        states = get_selected_states('5')
        self.assertEqual(states, ['selected', '', '', ''])

        states = get_selected_states('-1')
        self.assertEqual(states, ['selected', '', '', ''])

    def test_css_class_names(self):
        """Test that proper CSS class names are used."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain expected CSS classes
        self.assertIn('class="', html)
        self.assertIn('form-select', html)

    def test_htmx_attributes(self):
        """Test that HTMX attributes are present."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain HTMX attributes
        self.assertIn('hx-post', html)
        self.assertIn('hx-target', html)

    def test_dropdown_options(self):
        """Test that all dropdowns have the correct options."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain all option values
        self.assertIn('value="0"', html)
        self.assertIn('value="1"', html)
        self.assertIn('value="2"', html)
        self.assertIn('value="3"', html)

        # Should contain option text
        self.assertIn('&lt;None&gt;', html)  # HTML entity for <None>

    def test_debug_output(self):
        """Test that prints actual HTML output for debugging."""
        print("\n=== MAIN PAGE HTML OUTPUT ===")
        response = self.app.get('/')
        print(response.data.decode('utf-8')[:500] + "...")
        print("=== END MAIN PAGE HTML ===\n")

        print("=== CALLBACK ENDPOINT HTML OUTPUT ===")
        response = self.app.post('/callback/1', data={'pos1': '2'})
        print(response.data.decode('utf-8'))
        print("=== END CALLBACK ENDPOINT HTML ===\n")


if __name__ == '__main__':
    unittest.main()
