#!/usr/bin/env python3
"""
Unit tests for FILEUPLOADPRESERVE example.

Tests file upload input preservation functionality with hx-preserve attribute.
"""

import os
import tempfile
import unittest
from io import BytesIO
from unittest.mock import patch

from myapp import app, allowed_file, validate_form_data


class TestFileUploadPreserve(unittest.TestCase):
    """Test cases for file upload input preservation."""

    def setUp(self):
        """Set up test client and temporary directory."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
        self.app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB for testing
        self.client = self.app.test_client()

    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])

    def test_index_page(self):
        """Test that the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File Upload Input Preservation', response.data)
        self.assertIn(b'hx-preserve', response.data)

    def test_allowed_file_valid_extensions(self):
        """Test allowed file extensions."""
        valid_files = [
            'test.txt', 'document.pdf', 'image.png', 'photo.jpg',
            'picture.jpeg', 'animation.gif', 'doc.doc', 'document.docx',
            'archive.zip', 'compressed.rar'
        ]

        for filename in valid_files:
            with self.subTest(filename=filename):
                self.assertTrue(allowed_file(filename))

    def test_allowed_file_invalid_extensions(self):
        """Test invalid file extensions."""
        invalid_files = [
            'script.exe', 'malware.bat', 'virus.com', 'trojan.scr',
            'no_extension', '.hidden', 'double..ext'
        ]

        for filename in invalid_files:
            with self.subTest(filename=filename):
                self.assertFalse(allowed_file(filename))

    def test_validate_form_data_valid(self):
        """Test form validation with valid data."""
        # Create a mock file object
        file = BytesIO(b'test content')
        file.filename = 'test.txt'

        errors = validate_form_data('John Doe', 'john@example.com', file)
        self.assertEqual(len(errors), 0)

    def test_validate_form_data_invalid_name(self):
        """Test form validation with invalid name."""
        file = BytesIO(b'test content')
        file.filename = 'test.txt'

        # Empty name
        errors = validate_form_data('', 'john@example.com', file)
        self.assertIn('name', errors)

        # Too short name
        errors = validate_form_data('J', 'john@example.com', file)
        self.assertIn('name', errors)

        # Whitespace only
        errors = validate_form_data('   ', 'john@example.com', file)
        self.assertIn('name', errors)

    def test_validate_form_data_invalid_email(self):
        """Test form validation with invalid email."""
        file = BytesIO(b'test content')
        file.filename = 'test.txt'

        # Empty email
        errors = validate_form_data('John Doe', '', file)
        self.assertIn('email', errors)

        # Invalid email format
        errors = validate_form_data('John Doe', 'invalid-email', file)
        self.assertIn('email', errors)

    def test_validate_form_data_invalid_file(self):
        """Test form validation with invalid file."""
        # No file
        errors = validate_form_data('John Doe', 'john@example.com', None)
        self.assertIn('file', errors)

        # Empty filename
        file = BytesIO(b'test content')
        file.filename = ''
        errors = validate_form_data('John Doe', 'john@example.com', file)
        self.assertIn('file', errors)

        # Invalid file type
        file = BytesIO(b'test content')
        file.filename = 'script.exe'
        errors = validate_form_data('John Doe', 'john@example.com', file)
        self.assertIn('file', errors)

    def test_upload_successful(self):
        """Test successful file upload."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'file': (BytesIO(b'test content'), 'test.txt')
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Successful', response.data)
        self.assertIn(b'John Doe', response.data)
        self.assertIn(b'john@example.com', response.data)
        self.assertIn(b'test.txt', response.data)

    def test_upload_with_validation_errors(self):
        """Test upload with validation errors (file preserved)."""
        data = {
            'name': '',  # Invalid name
            'email': 'invalid-email',  # Invalid email
            'file': (BytesIO(b'test content'), 'test.txt')
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'hx-preserve', response.data)  # File input preserved
        self.assertIn(b'Name must be at least 2 characters', response.data)
        self.assertIn(b'Please enter a valid email', response.data)

    def test_upload_without_preserve_errors(self):
        """Test upload without preserve (file not preserved)."""
        data = {
            'name': '',  # Invalid name
            'email': 'invalid-email',  # Invalid email
            'file': (BytesIO(b'test content'), 'test.txt')
        }

        response = self.client.post('/upload-without-preserve', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'hx-preserve', response.data)  # File input NOT preserved
        self.assertIn(b'Name must be at least 2 characters', response.data)
        self.assertIn(b'Please enter a valid email', response.data)

    def test_upload_invalid_file_type(self):
        """Test upload with invalid file type."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'file': (BytesIO(b'test content'), 'script.exe')
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File type not allowed', response.data)

    def test_upload_no_file(self):
        """Test upload without file."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please select a file to upload', response.data)

    def test_upload_file_too_large(self):
        """Test upload with file too large."""
        # Create a new app instance with smaller file limit for testing
        test_app = app
        test_app.config['MAX_CONTENT_LENGTH'] = 1  # 1 byte limit
        test_client = test_app.test_client()

        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'file': (BytesIO(b'test content'), 'test.txt')
        }

        response = test_client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 413)
        self.assertIn(b'File Too Large', response.data)

    def test_form_preserves_values_on_error(self):
        """Test that form values are preserved on validation errors."""
        data = {
            'name': 'John Doe',
            'email': 'invalid-email',  # Invalid email
            'file': (BytesIO(b'test content'), 'test.txt')
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)

        # Check that name value is preserved
        self.assertIn(b'value="John Doe"', response.data)
        # Check that email value is preserved
        self.assertIn(b'value="invalid-email"', response.data)

    def test_security_headers(self):
        """Test that security headers are added."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-XSS-Protection'), '1; mode=block')

    def test_upload_directory_creation(self):
        """Test that upload directory is created if it doesn't exist."""
        # Remove upload directory
        import shutil
        if os.path.exists(self.app.config['UPLOAD_FOLDER']):
            shutil.rmtree(self.app.config['UPLOAD_FOLDER'])

        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'file': (BytesIO(b'test content'), 'test.txt')
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Successful', response.data)

        # Check that directory was created
        self.assertTrue(os.path.exists(self.app.config['UPLOAD_FOLDER']))

    def test_file_sanitization(self):
        """Test that filenames are properly sanitized."""
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'file': (BytesIO(b'test content'), '../../../etc/passwd.txt')  # Add .txt extension
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Upload Successful', response.data)

        # Check that file was saved with sanitized name
        files = os.listdir(self.app.config['UPLOAD_FOLDER'])
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0], 'etc_passwd.txt')  # Sanitized filename

    def test_multiple_validation_errors(self):
        """Test form with multiple validation errors."""
        data = {
            'name': 'J',  # Too short
            'email': 'invalid',  # Invalid format
            'file': (BytesIO(b'test content'), 'script.exe')  # Invalid type
        }

        response = self.client.post('/upload', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 200)

        # Check all error messages are present
        self.assertIn(b'Name must be at least 2 characters', response.data)
        self.assertIn(b'Please enter a valid email', response.data)
        self.assertIn(b'File type not allowed', response.data)

    def test_htmx_preserve_attribute_present(self):
        """Test that hx-preserve attribute is present in the main form."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check that hx-preserve is present in the first form
        self.assertIn(b'<input type="file"', response.data)
        self.assertIn(b'hx-preserve', response.data)

    def test_htmx_preserve_attribute_absent_in_second_form(self):
        """Test that hx-preserve attribute is absent in the second form."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Count occurrences of file input
        file_inputs = response.data.count(b'<input type="file"')
        self.assertEqual(file_inputs, 2)  # Two file inputs

        # Check that the first form has hx-preserve and second doesn't
        # Split the response by forms to check each one
        content = response.data.decode('utf-8')

        # Find the first form (with preserve)
        first_form_start = content.find('id="preserveForm"')
        first_form_end = content.find('</form>', first_form_start)
        first_form = content[first_form_start:first_form_end]

        # Find the second form (without preserve)
        second_form_start = content.find('id="noPreserveForm"')
        second_form_end = content.find('</form>', second_form_start)
        second_form = content[second_form_start:second_form_end]

        # Check that first form has hx-preserve
        self.assertIn('hx-preserve', first_form)

        # Check that second form does NOT have hx-preserve
        self.assertNotIn('hx-preserve', second_form)


if __name__ == '__main__':
    unittest.main()
