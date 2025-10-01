#!/usr/bin/env python3
"""
Unit tests for HTMX File Upload Example

Tests the file upload functionality including:
- Single and multiple file uploads
- Validation (file type, size, security)
- HTML response format (not JSON)
- File listing and deletion
"""

import unittest
import tempfile
import shutil
import os
from io import BytesIO
from pathlib import Path

# Import the Flask app
from myapp import app


class FileUploadTestCase(unittest.TestCase):
    """Test cases for file upload functionality."""

    def setUp(self):
        """Set up test client and temporary upload directory."""
        # Create a temporary directory for uploads
        self.test_upload_dir = tempfile.mkdtemp()
        app.config['UPLOAD_FOLDER'] = self.test_upload_dir
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        """Clean up temporary upload directory."""
        if os.path.exists(self.test_upload_dir):
            shutil.rmtree(self.test_upload_dir)

    # =========================================================================
    # Basic Upload Tests
    # =========================================================================

    def test_index_page_loads(self):
        """Test that the main page loads successfully."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'File Upload Example', response.data)
        self.assertIn(b'hx-post="/upload"', response.data)

    def test_successful_file_upload(self):
        """Test uploading a valid file returns success HTML."""
        data = {
            'file': (BytesIO(b'test file content'), 'test.pdf')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Successfully uploaded', html)
        self.assertIn('test.pdf', html)
        self.assertIn('class="success"', html)

    def test_file_saved_to_disk(self):
        """Test that uploaded file is actually saved."""
        data = {
            'file': (BytesIO(b'test content'), 'saved.txt')
        }
        self.client.post('/upload', data=data,
                        content_type='multipart/form-data')

        # Check file exists
        file_path = os.path.join(self.test_upload_dir, 'saved.txt')
        self.assertTrue(os.path.exists(file_path))

        # Check content
        with open(file_path, 'r') as f:
            self.assertEqual(f.read(), 'test content')

    # =========================================================================
    # Validation Tests
    # =========================================================================

    def test_no_file_provided(self):
        """Test error when no file is provided."""
        response = self.client.post('/upload', data={},
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn('No file provided', html)
        self.assertIn('class="error"', html)

    def test_empty_filename(self):
        """Test error when filename is empty."""
        data = {
            'file': (BytesIO(b'content'), '')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn('No file selected', html)

    def test_invalid_file_extension(self):
        """Test rejection of invalid file type."""
        data = {
            'file': (BytesIO(b'malicious code'), 'malware.exe')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn('not allowed', html)

    def test_file_too_large(self):
        """Test rejection of oversized file."""
        # Create file larger than 16MB limit
        large_content = b'x' * (17 * 1024 * 1024)
        data = {
            'file': (BytesIO(large_content), 'huge.pdf')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        # Should return 413 (Request Entity Too Large) or 400
        self.assertIn(response.status_code, [400, 413])

    def test_empty_file_rejected(self):
        """Test that empty files are rejected."""
        data = {
            'file': (BytesIO(b''), 'empty.pdf')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn('empty', html.lower())

    def test_filename_sanitization(self):
        """Test that dangerous filenames are sanitized."""
        data = {
            'file': (BytesIO(b'content'), '../../../etc/passwd')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        # Should reject due to invalid characters
        self.assertEqual(response.status_code, 400)

    # =========================================================================
    # Multiple File Upload Tests
    # =========================================================================

    def test_multiple_file_upload(self):
        """Test uploading multiple files at once."""
        data = {
            'files': [
                (BytesIO(b'file 1'), 'doc1.pdf'),
                (BytesIO(b'file 2'), 'doc2.txt'),
                (BytesIO(b'file 3'), 'image.png')
            ]
        }
        response = self.client.post('/upload-multiple', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('Uploaded 3 file', html)

    def test_multiple_files_with_errors(self):
        """Test multiple upload with some valid and some invalid files."""
        data = {
            'files': [
                (BytesIO(b'valid'), 'valid.pdf'),
                (BytesIO(b'invalid'), 'bad.exe'),  # Invalid extension
                (BytesIO(b'another valid'), 'good.txt')
            ]
        }
        response = self.client.post('/upload-multiple', data=data,
                                    content_type='multipart/form-data')

        html = response.get_data(as_text=True)
        # Should have uploaded 2 valid files
        self.assertIn('2 file', html)
        # Should show error for .exe file
        self.assertIn('bad.exe', html)

    def test_multiple_upload_no_files(self):
        """Test multiple upload with no files provided."""
        response = self.client.post('/upload-multiple', data={},
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn('No files provided', html)

    # =========================================================================
    # File Listing Tests
    # =========================================================================

    def test_list_files_empty(self):
        """Test listing files when directory is empty."""
        response = self.client.get('/files')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('No files', html)

    def test_list_files_with_content(self):
        """Test listing files after uploading."""
        # Upload a file first
        data = {'file': (BytesIO(b'test'), 'example.pdf')}
        self.client.post('/upload', data=data,
                        content_type='multipart/form-data')

        # List files
        response = self.client.get('/files')

        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn('example.pdf', html)
        self.assertIn('file-item', html)

    # =========================================================================
    # File Deletion Tests
    # =========================================================================

    def test_delete_file(self):
        """Test deleting an uploaded file."""
        # Upload a file
        data = {'file': (BytesIO(b'to delete'), 'delete-me.txt')}
        self.client.post('/upload', data=data,
                        content_type='multipart/form-data')

        # Verify it exists
        file_path = os.path.join(self.test_upload_dir, 'delete-me.txt')
        self.assertTrue(os.path.exists(file_path))

        # Delete it
        response = self.client.delete('/delete-file/delete-me.txt')
        self.assertEqual(response.status_code, 200)

        # Verify it's gone
        self.assertFalse(os.path.exists(file_path))

    def test_delete_nonexistent_file(self):
        """Test deleting a file that doesn't exist."""
        response = self.client.delete('/delete-file/nonexistent.pdf')

        # Should succeed (idempotent delete)
        self.assertEqual(response.status_code, 200)

    # =========================================================================
    # Security Tests
    # =========================================================================

    def test_allowed_file_types(self):
        """Test that all allowed file types are accepted."""
        allowed_types = [
            'image.png', 'photo.jpg', 'doc.pdf',
            'text.txt', 'archive.zip', 'data.csv'
        ]

        for filename in allowed_types:
            data = {'file': (BytesIO(b'content'), filename)}
            response = self.client.post('/upload', data=data,
                                        content_type='multipart/form-data')

            self.assertEqual(response.status_code, 200,
                           f"Failed to upload {filename}")

    def test_filename_with_spaces(self):
        """Test handling filename with spaces."""
        data = {
            'file': (BytesIO(b'content'), 'my document.pdf')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        # Should succeed (secure_filename handles spaces)
        self.assertEqual(response.status_code, 200)

        # Check that file was saved with sanitized name
        files = os.listdir(self.test_upload_dir)
        self.assertTrue(any('document' in f for f in files))

    def test_no_file_extension(self):
        """Test rejection of files without extension."""
        data = {
            'file': (BytesIO(b'content'), 'noextension')
        }
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        self.assertEqual(response.status_code, 400)
        html = response.get_data(as_text=True)
        self.assertIn('extension', html.lower())

    # =========================================================================
    # HTML Response Format Tests
    # =========================================================================

    def test_responses_are_html_not_json(self):
        """Test that responses are HTML fragments, not JSON."""
        data = {'file': (BytesIO(b'test'), 'test.pdf')}
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        # Should be HTML
        self.assertIn(b'<div', response.data)

        # Should NOT be JSON
        self.assertNotIn(b'{"', response.data)
        self.assertNotIn(b'"success":', response.data)

    def test_success_response_format(self):
        """Test that success responses have correct HTML structure."""
        data = {'file': (BytesIO(b'test'), 'test.pdf')}
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        html = response.get_data(as_text=True)

        # Should have success class
        self.assertIn('class="success"', html)

        # Should have checkmark emoji
        self.assertIn('✅', html)

        # Should show filename
        self.assertIn('test.pdf', html)

    def test_error_response_format(self):
        """Test that error responses have correct HTML structure."""
        data = {'file': (BytesIO(b'bad'), 'bad.exe')}
        response = self.client.post('/upload', data=data,
                                    content_type='multipart/form-data')

        html = response.get_data(as_text=True)

        # Should have error class
        self.assertIn('class="error"', html)

        # Should have X emoji
        self.assertIn('❌', html)


def run_tests():
    """Run all tests."""
    unittest.main()


if __name__ == '__main__':
    run_tests()

