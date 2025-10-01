#!/usr/bin/env python3
"""
HTMX File Upload Example

This example demonstrates file upload patterns using HTMX:
- hx-post: Send file upload requests to server
- hx-encoding="multipart/form-data": Proper form encoding for files
- htmx:xhr:progress event: Real-time upload progress tracking
- Progress bar: Visual feedback using HTML5 progress element

Based on the official HTMX file-upload example at:
https://htmx.org/examples/file-upload/

Follows Development Guiding Light principles for educational clarity.
"""

import os
import mimetypes
from pathlib import Path
from flask import Flask, render_template, request
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


@app.route('/')
def index():
    """Main page with file upload interface."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle single file upload with validation."""
    if 'file' not in request.files:
        return '<div class="error">❌ No file provided</div>', 400

    file = request.files['file']

    if file.filename == '':
        return '<div class="error">❌ No file selected</div>', 400

    # Validate file
    validation_result = validate_file(file)
    if not validation_result['valid']:
        return f'<div class="error">❌ {validation_result["error"]}</div>', 400

    # Use secure filename
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    try:
        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file
        file.save(file_path)

        # Verify file was saved
        if not os.path.exists(file_path):
            return '<div class="error">❌ File was not saved to disk</div>', 500

        # Get file info
        file_size = os.path.getsize(file_path)
        size_kb = file_size / 1024

        return f'''<div class="success">
            ✅ Successfully uploaded <strong>{filename}</strong>
            ({size_kb:.1f} KB)
        </div>'''

    except Exception as e:
        # Clean up partial upload
        if os.path.exists(file_path):
            os.remove(file_path)
        return f'<div class="error">❌ Upload failed: {str(e)}</div>', 500


@app.route('/upload-multiple', methods=['POST'])
def upload_multiple_files():
    """Handle multiple file uploads."""
    if 'files' not in request.files:
        return '<div class="error">❌ No files provided</div>', 400

    files = request.files.getlist('files')
    uploaded = []
    errors = []

    for file in files:
        if file.filename == '':
            continue

        # Validate file
        validation_result = validate_file(file)
        if not validation_result['valid']:
            errors.append(f"{file.filename}: {validation_result['error']}")
            continue

        # Use secure filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            # Ensure upload directory exists
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            # Save file
            file.save(file_path)

            # Verify file was saved
            if not os.path.exists(file_path):
                errors.append(f"{file.filename}: Not saved to disk")
                continue

            # Get file info
            file_size = os.path.getsize(file_path)
            uploaded.append(f"{filename} ({file_size/1024:.1f} KB)")

        except Exception as e:
            errors.append(f"{file.filename}: {str(e)}")

    # Build response HTML
    html = '<div class="multi-result">'
    if uploaded:
        html += f'<div class="success">✅ Uploaded {len(uploaded)} file(s):<ul>'
        for file_info in uploaded:
            html += f'<li>{file_info}</li>'
        html += '</ul></div>'
    if errors:
        html += '<div class="error">❌ Errors:<ul>'
        for error in errors:
            html += f'<li>{error}</li>'
        html += '</ul></div>'
    html += '</div>'

    return html


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
            'error': f'File type .{extension} not allowed'
        }

    # Check file size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > app.config['MAX_CONTENT_LENGTH']:
        return {'valid': False, 'error': 'File too large (max 16MB)'}

    if size == 0:
        return {'valid': False, 'error': 'File is empty'}

    # Check for suspicious filenames
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\', '..']
    if any(char in filename for char in invalid_chars):
        return {'valid': False, 'error': 'Invalid characters in filename'}

    return {'valid': True}


@app.route('/files')
def list_files():
    """List uploaded files."""
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            if filename.startswith('.'):
                continue

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            stat = os.stat(file_path)
            file_type = mimetypes.guess_type(filename)[0] or 'unknown'

            # Get icon based on type
            if file_type.startswith('image/'):
                icon = '🖼️'
            elif file_type.startswith('text/') or 'pdf' in file_type:
                icon = '📄'
            elif 'zip' in filename or 'rar' in filename:
                icon = '📦'
            else:
                icon = '📁'

            files.append({
                'icon': icon,
                'filename': filename,
                'size': stat.st_size / 1024,  # KB
                'type': file_type
            })

        # Sort by filename
        files.sort(key=lambda x: x['filename'])

        # Build HTML
        if not files:
            return '<div class="no-files">No files uploaded yet</div>'

        html = '<div class="file-list">'
        for f in files:
            html += f'''
            <div class="file-item">
                <span class="file-icon">{f["icon"]}</span>
                <div class="file-info">
                    <div class="file-name">{f["filename"]}</div>
                    <div class="file-meta">{f["size"]:.1f} KB • {f["type"]}</div>
                </div>
                <button class="btn-delete"
                        hx-delete="/delete-file/{f["filename"]}"
                        hx-target="#file-list"
                        hx-confirm="Delete {f["filename"]}?">
                    🗑️
                </button>
            </div>
            '''
        html += '</div>'
        return html

    except Exception as e:
        return f'<div class="error">Error listing files: {str(e)}</div>'


@app.route('/delete-file/<filename>', methods=['DELETE'])
def delete_file(filename):
    """Delete uploaded file."""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Return updated file list
        return list_files()

    except Exception as e:
        return f'<div class="error">Error deleting file: {str(e)}</div>'


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(error):
    """Handle file too large errors."""
    return '<div class="error">❌ File too large. Maximum size is 16MB.</div>', 413


if __name__ == '__main__':
    app.run(debug=True)
