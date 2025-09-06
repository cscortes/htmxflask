#!/usr/bin/env python3
"""
HTMX File Upload Example

This example demonstrates modern file upload patterns using HTMX:
- hx-post: Send file upload requests to server
- hx-encoding="multipart/form-data": Proper form encoding for files
- hx-indicator: Show upload progress and loading states
- Drag and drop: HTML5 drag and drop API integration
- Progress tracking: Real-time upload progress indicators

Based on the official HTMX file-upload example.
Follows Development Guiding Light principles for educational clarity.
"""

import os
import uuid
import time
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# File upload configuration
app.config['UPLOAD_FOLDER'] = upload_dir
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {
    # Images
    'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg',
    # Documents
    'pdf', 'doc', 'docx', 'txt', 'rtf',
    # Archives
    'zip', 'rar', '7z', 'tar', 'gz',
    # Other
    'csv', 'json', 'xml'
}

# Create upload directory if it doesn't exist
Path(upload_dir).mkdir(exist_ok=True)

# Store active uploads for progress tracking
active_uploads = {}


@app.route('/')
def index():
    """Main page with file upload interface."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle single file upload with validation and progress tracking."""
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file provided'
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400

    # Validate file
    validation_result = validate_file(file)
    if not validation_result['valid']:
        return jsonify({
            'success': False,
            'error': validation_result['error']
        }), 400

    # Generate unique filename
    original_filename = secure_filename(file.filename)
    file_extension = Path(original_filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

    try:
        # Save file
        file.save(file_path)

        # Get file info
        file_size = os.path.getsize(file_path)
        file_type = mimetypes.guess_type(original_filename)[0] or 'application/octet-stream'

        return jsonify({
            'success': True,
            'filename': original_filename,
            'unique_filename': unique_filename,
            'size': file_size,
            'type': file_type,
            'message': f'Successfully uploaded {original_filename}'
        })

    except Exception as e:
        # Clean up partial upload
        if os.path.exists(file_path):
            os.remove(file_path)

        return jsonify({
            'success': False,
            'error': f'Upload failed: {str(e)}'
        }), 500


@app.route('/upload-multiple', methods=['POST'])
def upload_multiple_files():
    """Handle multiple file uploads."""
    if 'files' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No files provided'
        }), 400

    files = request.files.getlist('files')
    results = []
    errors = []

    for file in files:
        if file.filename == '':
            continue

        # Validate file
        validation_result = validate_file(file)
        if not validation_result['valid']:
            errors.append({
                'filename': file.filename,
                'error': validation_result['error']
            })
            continue

        # Generate unique filename
        original_filename = secure_filename(file.filename)
        file_extension = Path(original_filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        try:
            # Save file
            file.save(file_path)

            # Get file info
            file_size = os.path.getsize(file_path)
            file_type = mimetypes.guess_type(original_filename)[0] or 'application/octet-stream'

            results.append({
                'filename': original_filename,
                'unique_filename': unique_filename,
                'size': file_size,
                'type': file_type
            })

        except Exception as e:
            errors.append({
                'filename': file.filename,
                'error': f'Upload failed: {str(e)}'
            })

    return jsonify({
        'success': len(results) > 0,
        'uploaded': results,
        'errors': errors,
        'message': f'Uploaded {len(results)} files successfully'
    })


@app.route('/validate-file', methods=['POST'])
def validate_file_endpoint():
    """Validate file before upload."""
    if 'file' not in request.files:
        return jsonify({
            'valid': False,
            'error': 'No file provided'
        })

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            'valid': False,
            'error': 'No file selected'
        })

    validation_result = validate_file(file)
    return jsonify(validation_result)


def validate_file(file):
    """Validate uploaded file for security and constraints."""
    filename = file.filename

    # Check file extension
    if '.' not in filename:
        return {'valid': False, 'error': 'File must have an extension'}

    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in app.config['ALLOWED_EXTENSIONS']:
        return {
            'valid': False,
            'error': f'File type .{extension} not allowed. Allowed types: {", ".join(sorted(app.config["ALLOWED_EXTENSIONS"]))}'
        }

    # Check file size (additional check beyond MAX_CONTENT_LENGTH)
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > app.config['MAX_CONTENT_LENGTH']:
        return {'valid': False, 'error': 'File too large'}

    # Basic security checks
    if size == 0:
        return {'valid': False, 'error': 'File is empty'}

    # Check for suspicious filenames (path traversal and invalid characters)
    if any(char in filename for char in ['<', '>', ':', '"', '|', '?', '*', '/', '\\', '..']):
        return {'valid': False, 'error': 'Invalid characters in filename'}

    return {'valid': True}


@app.route('/files')
def list_files():
    """List uploaded files (for demonstration)."""
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith('.'):
                continue

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            stat = os.stat(file_path)

            files.append({
                'filename': filename,
                'size': stat.st_size,
                'modified': stat.st_mtime,
                'type': mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            })

        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/delete-file/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete uploaded file."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return jsonify({'success': True, 'message': 'File deleted'})
        else:
            return jsonify({'success': False, 'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    """Handle file too large errors."""
    return jsonify({
        'success': False,
        'error': 'File too large. Maximum size is 16MB.'
    }), 413


if __name__ == '__main__':
    app.run(debug=True)
