#!/usr/bin/env python3
"""
FILEUPLOADPRESERVE - File Upload Input Preservation Example

This example demonstrates how to preserve file inputs after form errors
using HTMX's hx-preserve attribute, based on:
https://htmx.org/examples/file-upload-input/

Key HTMX Features:
- hx-preserve: Preserves file input values after form errors
- hx-post: Handles form submission via AJAX
- hx-target: Targets specific elements for content replacement
- hx-swap: Controls how content is replaced

User Story:
As a user uploading files with additional form data, I want my file selection
to be preserved when validation errors occur, so I don't have to re-select
the file after fixing form errors.
"""

import os
import tempfile
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip', 'rar'
}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def validate_form_data(name, email, file):
    """Validate form data and return errors."""
    errors = {}

    # Validate name
    if not name or len(name.strip()) < 2:
        errors['name'] = 'Name must be at least 2 characters long'

    # Validate email
    if not email or '@' not in email:
        errors['email'] = 'Please enter a valid email address'

    # Validate file
    if not file or file.filename == '':
        errors['file'] = 'Please select a file to upload'
    elif not allowed_file(file.filename):
        errors['file'] = f'File type not allowed. Allowed types: {", ".join(app.config["ALLOWED_EXTENSIONS"])}'

    return errors


@app.route('/')
def index():
    """Main page with file upload form."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle file upload with form validation.
    Returns HTML with errors or success message.
    """
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    file = request.files.get('file')

    # Validate form data
    errors = validate_form_data(name, email, file)

    if errors:
        # Return form with errors - file input will be preserved by hx-preserve
        return render_template('form_with_errors.html',
                             name=name,
                             email=email,
                             errors=errors)

    try:
        # Process successful upload
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file
        file.save(file_path)

        # Get file info
        file_size = os.path.getsize(file_path)
        size_kb = file_size / 1024

        # Return success message
        return f'''<div class="success-message">
            <h3>✅ Upload Successful!</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>File:</strong> {filename} ({size_kb:.1f} KB)</p>
            <button onclick="location.reload()" class="btn btn-primary">Upload Another File</button>
        </div>'''

    except Exception as e:
        # Return error message
        return f'''<div class="error-message">
            <h3>❌ Upload Failed</h3>
            <p>Error: {str(e)}</p>
            <button onclick="location.reload()" class="btn btn-secondary">Try Again</button>
        </div>''', 500


@app.route('/upload-without-preserve', methods=['POST'])
def upload_file_without_preserve():
    """
    Handle file upload without preserving file input.
    This demonstrates the difference when hx-preserve is not used.
    """
    # Get form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    file = request.files.get('file')

    # Validate form data
    errors = validate_form_data(name, email, file)

    if errors:
        # Return form with errors - file input will NOT be preserved
        return render_template('form_with_errors_no_preserve.html',
                             name=name,
                             email=email,
                             errors=errors)

    try:
        # Process successful upload
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure upload directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Save file
        file.save(file_path)

        # Get file info
        file_size = os.path.getsize(file_path)
        size_kb = file_size / 1024

        # Return success message
        return f'''<div class="success-message">
            <h3>✅ Upload Successful!</h3>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>File:</strong> {filename} ({size_kb:.1f} KB)</p>
            <button onclick="location.reload()" class="btn btn-primary">Upload Another File</button>
        </div>'''

    except Exception as e:
        # Return error message
        return f'''<div class="error-message">
            <h3>❌ Upload Failed</h3>
            <p>Error: {str(e)}</p>
            <button onclick="location.reload()" class="btn btn-secondary">Try Again</button>
        </div>''', 500


@app.errorhandler(RequestEntityTooLarge)
def handle_file_too_large(e):
    """Handle file size limit exceeded."""
    return '''<div class="error-message">
        <h3>❌ File Too Large</h3>
        <p>File size exceeds the 16MB limit.</p>
        <button onclick="location.reload()" class="btn btn-secondary">Try Again</button>
    </div>''', 413


@app.after_request
def add_security_headers(response):
    """Add security headers for HTMX compatibility."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response


if __name__ == '__main__':
    app.run(debug=True, port=5007)
