#!/usr/bin/env python3
"""
Unit tests for ACTIVESEARCH example.

Tests the active search functionality with HTMX patterns:
- hx-post: Send search requests
- hx-trigger: Real-time search on input
- hx-target: Update results table
- hx-indicator: Show loading state
"""

import unittest
from myapp import app, User


class TestActiveSearch(unittest.TestCase):
    """Test suite for ACTIVESEARCH functionality."""

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_index_page_loads(self):
        """Test that the main page loads correctly."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Contacts', response.data)

    def test_search_endpoint_exists(self):
        """Test that the search endpoint responds."""
        response = self.app.post('/search/', data={'search': 'john'})
        self.assertEqual(response.status_code, 200)

    def test_search_with_valid_term(self):
        """Test search with a valid search term."""
        response = self.app.post('/search/', data={'search': 'john'})
        self.assertEqual(response.status_code, 200)
        # Should find John Smith
        self.assertIn(b'John', response.data)
        self.assertIn(b'Smith', response.data)

    def test_search_with_empty_term(self):
        """Test search with empty term returns all users."""
        response = self.app.post('/search/', data={'search': ''})
        self.assertEqual(response.status_code, 200)
        # Should return all users
        self.assertIn(b'John', response.data)
        self.assertIn(b'Jane', response.data)
        self.assertIn(b'Bob', response.data)

    def test_search_with_whitespace_only(self):
        """Test search with whitespace-only term returns all users."""
        response = self.app.post('/search/', data={'search': '   '})
        self.assertEqual(response.status_code, 200)
        # Should return all users
        self.assertIn(b'John', response.data)
        self.assertIn(b'Jane', response.data)

    def test_search_with_no_results(self):
        """Test search with term that has no matches."""
        response = self.app.post('/search/',
                                data={'search': 'xyz123nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No users found', response.data)

    def test_search_case_insensitive(self):
        """Test that search is case insensitive."""
        response = self.app.post('/search/', data={'search': 'JANE'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane', response.data)

    def test_search_in_email(self):
        """Test search works in email addresses."""
        response = self.app.post('/search/', data={'search': 'company.com'})
        self.assertEqual(response.status_code, 200)
        # Should find users with company.com email
        self.assertIn(b'company.com', response.data)

    def test_search_in_last_name(self):
        """Test search works in last names."""
        response = self.app.post('/search/', data={'search': 'Smith'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Smith', response.data)

    def test_html_structure_validation(self):
        """Test that HTML structure matches expected patterns."""
        response = self.app.post('/search/', data={'search': 'john'})
        html = response.data.decode('utf-8')

        # Should contain table row structure
        self.assertIn('<tr>', html)
        self.assertIn('</tr>', html)
        self.assertIn('<td>', html)
        self.assertIn('</td>', html)

    def test_user_search_method(self):
        """Test the User.search method functionality."""
        user = User("Test", "User", "test@example.com")

        # Test exact match
        self.assertTrue(user.search("Test"))
        self.assertTrue(user.search("User"))
        self.assertTrue(user.search("test@example.com"))

        # Test case insensitive
        self.assertTrue(user.search("test"))
        self.assertTrue(user.search("USER"))

        # Test partial match
        self.assertTrue(user.search("exampl"))

        # Test no match
        self.assertFalse(user.search("xyz"))
        self.assertFalse(user.search("nonexistent"))

    def test_user_search_with_none(self):
        """Test User.search method with None input."""
        user = User("Test", "User", "test@example.com")
        self.assertFalse(user.search(None))

    def test_user_id_increment(self):
        """Test that User IDs increment properly."""
        # Reset the counter for testing
        User.id = 0

        user1 = User("First", "User", "first@test.com")
        user2 = User("Second", "User", "second@test.com")

        self.assertEqual(user1.id, 1)
        self.assertEqual(user2.id, 2)

    def test_css_class_names(self):
        """Test that proper CSS class names are used."""
        response = self.app.get('/')
        html = response.data.decode('utf-8')

        # Should contain expected CSS classes
        self.assertIn('class="', html)
        self.assertIn('htmx-indicator', html)

    def test_debug_output(self):
        """Test that prints actual HTML output for debugging."""
        print("\n=== MAIN PAGE HTML OUTPUT ===")
        response = self.app.get('/')
        print(response.data.decode('utf-8')[:500] + "...")
        print("=== END MAIN PAGE HTML ===\n")

        print("=== SEARCH RESULTS HTML OUTPUT ===")
        response = self.app.post('/search/', data={'search': 'john'})
        print(response.data.decode('utf-8'))
        print("=== END SEARCH RESULTS HTML ===\n")


if __name__ == '__main__':
    unittest.main()
