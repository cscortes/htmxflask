#!/usr/bin/env python3
"""
Unit tests for HTMX File Upload Example
"""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from myapp import app


class FileUploadTestCase(unittest.TestCase):
    """Test cases for file upload functionality."""

    def setUp(self):
        """Set up test environment before each test."""
        self.upload_dir = tempfile.mkdtemp()
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = self.upload_dir
        self.client = app.test_client()

    def tearDown(self):
        """Clean up after each test."""
        # Clean up uploaded files
        try:
            for filename in os.listdir(self.upload_dir):
                file_path = os.path.join(self.upload_dir, filename)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            os.rmdir(self.upload_dir)
        except (OSError, FileNotFoundError):
            pass  # Directory might already be cleaned up

    def test_index_page(self):
        """Test the main page loads correctly."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response_text = response.get_data(as_text=True)
        self.assertIn('File Upload Example', response_text)
        self.assertIn('upload-zone', response_text)

    def test_successful_file_upload(self):
        """Test successful file upload."""
        # Create a test file
        test_file = BytesIO(b'test file content')
        test_file.filename = 'test.txt'

        response = self.client.post('/upload', data={'file': (test_file, 'test.txt')})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['filename'], 'test.txt')
        self.assertIn('Successfully uploaded', response_data['message'])

        # Check file was saved
        files = os.listdir(app.config['UPLOAD_FOLDER'])
        self.assertEqual(len(files), 1)
        self.assertTrue(files[0].endswith('.txt'))

    def test_upload_without_file(self):
        """Test upload request without file."""
        response = self.client.post('/upload', data={})
        self.assertEqual(response.status_code, 400)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('No file provided', response_data['error'])

    def test_upload_empty_filename(self):
        """Test upload with empty filename."""
        test_file = BytesIO(b'content')
        test_file.filename = ''

        response = self.client.post('/upload', data={'file': (test_file, '')})
        self.assertEqual(response.status_code, 400)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('No file selected', response_data['error'])

    def test_invalid_file_extension(self):
        """Test upload with invalid file extension."""
        test_file = BytesIO(b'test content')
        test_file.filename = 'test.exe'

        response = self.client.post('/upload', data={'file': (test_file, 'test.exe')})
        self.assertEqual(response.status_code, 400)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('not allowed', response_data['error'])

    def test_file_too_large(self):
        """Test upload with file exceeding size limit."""
        # Create a large file (over 16MB)
        large_content = b'x' * (17 * 1024 * 1024)  # 17MB
        test_file = BytesIO(large_content)
        test_file.filename = 'large.txt'

        response = self.client.post('/upload', data={'file': (test_file, 'large.txt')})
        self.assertEqual(response.status_code, 413)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('too large', response_data['error'])

    def test_valid_image_upload(self):
        """Test upload of valid image file."""
        # Create a mock image file
        test_file = BytesIO(b'fake image content')
        test_file.filename = 'test.png'

        response = self.client.post('/upload', data={'file': (test_file, 'test.png')})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['filename'], 'test.png')

    def test_valid_document_upload(self):
        """Test upload of valid document file."""
        test_file = BytesIO(b'document content')
        test_file.filename = 'test.pdf'

        response = self.client.post('/upload', data={'file': (test_file, 'test.pdf')})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['filename'], 'test.pdf')

    def test_multiple_file_upload(self):
        """Test multiple file upload."""
        file1 = BytesIO(b'content1')
        file1.filename = 'test1.txt'
        file2 = BytesIO(b'content2')
        file2.filename = 'test2.txt'

        response = self.client.post('/upload-multiple',
                                  data={'files': [(file1, 'test1.txt'), (file2, 'test2.txt')]})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertEqual(len(response_data['uploaded']), 2)
        self.assertIn('Uploaded 2 files', response_data['message'])

    def test_multiple_files_with_errors(self):
        """Test multiple file upload with some valid and some invalid files."""
        file1 = BytesIO(b'content1')
        file1.filename = 'test1.txt'
        file2 = BytesIO(b'content2')
        file2.filename = 'test2.exe'  # Invalid extension

        response = self.client.post('/upload-multiple',
                                  data={'files': [(file1, 'test1.txt'), (file2, 'test2.exe')]})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])  # At least one file uploaded
        self.assertEqual(len(response_data['uploaded']), 1)
        self.assertEqual(len(response_data['errors']), 1)

    def test_file_validation_endpoint(self):
        """Test file validation endpoint."""
        test_file = BytesIO(b'test content')
        test_file.filename = 'test.txt'

        response = self.client.post('/validate-file', data={'file': (test_file, 'test.txt')})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['valid'])

    def test_invalid_file_validation(self):
        """Test validation of invalid file."""
        test_file = BytesIO(b'test content')
        test_file.filename = 'test.exe'

        response = self.client.post('/validate-file', data={'file': (test_file, 'test.exe')})
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertFalse(response_data['valid'])
        self.assertIn('not allowed', response_data['error'])

    def test_list_files(self):
        """Test listing uploaded files."""
        # First upload a file
        test_file = BytesIO(b'test content')
        test_file.filename = 'test.txt'
        upload_response = self.client.post('/upload', data={'file': (test_file, 'test.txt')})
        upload_data = upload_response.get_json()
        self.assertTrue(upload_data['success'])

        # Then list files
        response = self.client.get('/files')
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertIn('files', response_data)

        # Should have at least one file
        self.assertGreaterEqual(len(response_data['files']), 1)

        # Check that at least one file has the expected properties
        found_file = False
        for file_info in response_data['files']:
            if file_info.get('size', 0) > 0:
                found_file = True
                break

        self.assertTrue(found_file, "No valid files found in list")

    def test_delete_file(self):
        """Test deleting uploaded file."""
        # First upload a file
        test_file = BytesIO(b'test content')
        test_file.filename = 'test.txt'
        upload_response = self.client.post('/upload', data={'file': (test_file, 'test.txt')})
        upload_data = upload_response.get_json()
        filename = upload_data['unique_filename']

        # Then delete it
        response = self.client.delete(f'/delete-file/{filename}')
        self.assertEqual(response.status_code, 200)

        response_data = response.get_json()
        self.assertTrue(response_data['success'])
        self.assertIn('deleted', response_data['message'])

    def test_delete_nonexistent_file(self):
        """Test deleting non-existent file."""
        response = self.client.delete('/delete-file/nonexistent.txt')
        self.assertEqual(response.status_code, 404)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('not found', response_data['error'])

    def test_security_filename_sanitization(self):
        """Test that dangerous filenames are rejected."""
        test_file = BytesIO(b'test content')
        test_file.filename = '../../dangerous.txt'

        response = self.client.post('/upload', data={'file': (test_file, '../../dangerous.txt')})
        self.assertEqual(response.status_code, 400)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('Invalid characters', response_data['error'])

    def test_empty_file_rejection(self):
        """Test that empty files are rejected."""
        test_file = BytesIO(b'')  # Empty file
        test_file.filename = 'empty.txt'

        response = self.client.post('/upload', data={'file': (test_file, 'empty.txt')})
        self.assertEqual(response.status_code, 400)

        response_data = response.get_json()
        self.assertFalse(response_data['success'])
        self.assertIn('empty', response_data['error'])

    def test_response_content_type(self):
        """Test that responses have correct content type."""
        # Test main page
        response = self.client.get('/')
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')

        # Test upload endpoint
        test_file = BytesIO(b'test')
        test_file.filename = 'test.txt'
        response = self.client.post('/upload', data={'file': (test_file, 'test.txt')})
        self.assertEqual(response.content_type, 'application/json')

    def test_htmx_attributes_present(self):
        """Test that HTMX attributes are present in the HTML."""
        response = self.client.get('/')
        html = response.get_data(as_text=True)

        # Check for HTMX upload attributes
        self.assertIn('hx-post="/upload"', html)
        self.assertIn('hx-encoding="multipart/form-data"', html)
        self.assertIn('hx-indicator="#upload-indicator"', html)
        self.assertIn('hx-target="#upload-result"', html)


if __name__ == '__main__':
    unittest.main()
