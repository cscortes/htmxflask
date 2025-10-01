#!/usr/bin/env python3
"""
DIALOGS Example - HTMX Dialogs with hx-prompt and hx-confirm

This example demonstrates native browser dialogs using HTMX:
- hx-prompt: Native browser prompt dialog for user input
- hx-confirm: Native browser confirmation dialog
- HX-Prompt header: Server receives user input from prompt
- hx-target: Target elements for response display

Based on: https://htmx.org/examples/dialogs/
"""

from flask import Flask, render_template, request, jsonify
import os
import tempfile
# import flask.jsonify

app = Flask(__name__)

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

# Store responses for demonstration
responses = []

@app.route('/')
def index():
    """Main page showing dialog examples"""
    return render_template('index.html', responses=responses)

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission with prompt and confirm dialogs"""
    print(f"DEBUG: Received request with headers: {dict(request.headers)}")

    # Get user input from HX-Prompt header (from hx-prompt dialog)
    user_input = request.headers.get('HX-Prompt', '')
    print(f"DEBUG: User input from prompt: '{user_input}'")

    # Create response message
    if user_input:
        response_text = f"User entered <i>{user_input}</i>"
    else:
        response_text = "No input provided"

    # Add to responses list for display
    responses.append({
        'text': response_text,
        'timestamp': 'Just now'
    })

    print(f"DEBUG: Added response: {response_text}")
    print(f"DEBUG: Total responses: {len(responses)}")

    return response_text

@app.route('/delete', methods=['POST'])
def delete():
    """Handle deletion with confirmation dialog"""
    print("DEBUG: Delete request received")

    # Clear all responses
    responses.clear()

    print("DEBUG: All responses cleared")

    return "All responses cleared!"

@app.route('/clear', methods=['POST'])
def clear():
    """Handle clearing with confirmation dialog"""
    print("DEBUG: Clear request received")

    # Clear all responses
    responses.clear()

    print("DEBUG: All responses cleared")

    return "Responses cleared successfully!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
