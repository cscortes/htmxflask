#!/usr/bin/env python3
"""
Unit tests for HTMX Lazy Loading Example
"""

import unittest
from unittest.mock import patch
from myapp import app
import time


class LazyLoadTestCase(unittest.TestCase):
    """Test cases for the lazy loading functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_index_page(self):
        """Test the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('Lazy Loading Example', response_text)
        self.assertIn('graph-container', response_text)
        self.assertIn('Loading analytics data', response_text)

    @patch('myapp.time.sleep')  # Mock sleep to speed up tests
    def test_graph_endpoint(self, mock_sleep):
        """Test the graph endpoint returns content correctly."""
        mock_sleep.return_value = None  # Skip the actual sleep

        response = self.client.get('/graph')
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)

        # Check for expected content
        self.assertIn('Monthly Revenue Analytics', response_text)
        self.assertIn('Interactive chart showing', response_text)
        self.assertIn('graph-container', response_text)
        self.assertIn('data-table', response_text)

        # Check for revenue data
        self.assertIn('$12,500', response_text)
        self.assertIn('$22,500', response_text)
        self.assertIn('+12%', response_text)
        self.assertIn('-2.1%', response_text)

        # Verify sleep was called with correct delay
        mock_sleep.assert_called_once_with(1.5)

    def test_graph_content_structure(self):
        """Test that the graph response has correct HTML structure."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for proper HTML structure
            self.assertIn('<div class="graph-container">', html)
            self.assertIn('<table class="data-table"', html)
            self.assertIn('<th scope="col">Month</th>', html)
            self.assertIn('<th scope="col">Revenue ($)</th>', html)
            self.assertIn('<th scope="col">Growth</th>', html)
            self.assertIn('role="table"', html)
            self.assertIn('aria-label="Revenue metrics"', html)

    def test_monthly_data_display(self):
        """Test that monthly data is displayed correctly."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for all months
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                     'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            for month in months:
                self.assertIn(f'<td>{month}</td>', html)

    def test_revenue_formatting(self):
        """Test that revenue values are properly formatted."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for comma-formatted numbers
            self.assertIn('$12,500', html)
            self.assertIn('$13,200', html)
            self.assertIn('$22,500', html)

    def test_growth_indicators(self):
        """Test that growth indicators are displayed correctly."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for growth classes
            self.assertIn('growth-positive', html)
            self.assertIn('growth-negative', html)

            # Check for specific growth values
            self.assertIn('+12%', html)
            self.assertIn('-2.1%', html)
            self.assertIn('+10.5%', html)

    def test_chart_visualization(self):
        """Test that the bar chart is included in the response."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for chart elements
            self.assertIn('bar-chart', html)
            self.assertIn('bar-item', html)
            self.assertIn('bar-label', html)
            self.assertIn('Revenue Trend', html)

    def test_htmx_attributes_present(self):
        """Test that HTMX attributes are present in the HTML."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for HTMX attributes
        self.assertIn('hx-get="/graph"', html)
        self.assertIn('hx-trigger="load"', html)
        self.assertIn('hx-indicator="#loading"', html)

    def test_loading_indicator(self):
        """Test that loading indicator is present."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for loading indicator
        self.assertIn('loading-indicator', html)
        self.assertIn('htmx-indicator', html)
        self.assertIn('Loading analytics data', html)
        self.assertIn('bars.svg', html)

    def test_graph_endpoint_timing(self):
        """Test that the graph endpoint has the expected delay."""
        with patch('myapp.time.sleep') as mock_sleep:
            mock_sleep.return_value = None
            self.client.get('/graph')

        # Verify sleep was called (simulating delay)
        mock_sleep.assert_called_once_with(1.5)

    def test_response_content_type(self):
        """Test that responses have correct content type."""
        # Test main page
        response = self.client.get('/')
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

        # Test graph endpoint
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            self.assertEqual(response.content_type, 'text/html; charset=utf-8')

    def test_graph_data_integrity(self):
        """Test that graph data maintains integrity."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Count table rows (should be 12 months + header)
            self.assertEqual(html.count('<tr>'), 13)  # 12 data rows + 1 header row

            # Count data cells using regex to match complete elements (3 columns × 12 rows)
            import re
            td_count = len(re.findall(r'<td[^>]*>.*?</td>', html, re.DOTALL))
            self.assertEqual(td_count, 36)  # 3 columns × 12 rows

    def test_accessibility_attributes(self):
        """Test that accessibility attributes are present."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for ARIA labels and roles
            self.assertIn('role="table"', html)
            self.assertIn('aria-label="Revenue metrics"', html)
            self.assertIn('scope="col"', html)

    def test_css_classes_present(self):
        """Test that CSS classes for styling are present."""
        with patch('myapp.time.sleep'):
            response = self.client.get('/graph')
            html = response.get_data(as_text=True)

            # Check for CSS classes
            self.assertIn('graph-container', html)
            self.assertIn('graph-title', html)
            self.assertIn('graph-description', html)
            self.assertIn('data-table', html)
            self.assertIn('revenue', html)
            self.assertIn('growth', html)
            self.assertIn('chart-container', html)
            self.assertIn('bar-chart', html)


if __name__ == '__main__':
    unittest.main()
