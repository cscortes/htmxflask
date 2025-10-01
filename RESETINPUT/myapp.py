

#!/usr/bin/env python3
"""
RESETINPUT - Reset User Input Example

This example demonstrates how to reset form inputs after successful requests
using HTMX's hx-on::after-request event, based on:
https://htmx.org/examples/reset-user-input/

Key HTMX Features:
- hx-on::after-request: Execute JavaScript after HTMX request completes
- hx-post: Handle form submission via AJAX
- hx-target: Target specific elements for content replacement
- hx-swap: Control how content is replaced (afterbegin for prepending)
- hx-include: Include specific elements in form data

User Story:
As a user adding notes, I want the input field to automatically clear after
successfully adding a note, so I can quickly add multiple notes without
manually clearing the field each time.
"""

import os
import tempfile
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for notes (in production, use a database)
notes = []

@app.route('/')
def index():
    """Render the main page with the note form and existing notes."""
    return render_template('index.html', notes=notes)

@app.route('/note', methods=['POST'])
def add_note():
    """
    Add a new note and return HTML fragment for the new note.
    This endpoint is called via HTMX and returns HTML to be inserted.
    """
    note_text = request.form.get('note-text', '').strip()
    print(f"DEBUG: Received note text: '{note_text}'")

    if not note_text:
        # Return error message if note is empty
        print("DEBUG: Empty note, returning 400 error")
        return '<li class="error">Note cannot be empty</li>', 400

    # Create new note with timestamp
    note = {
        'id': len(notes) + 1,
        'text': note_text,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # Add to notes list
    notes.append(note)
    print(f"DEBUG: Added note, total notes: {len(notes)}")

    # Return HTML fragment for the new note
    html_response = f'''<li class="note-item">
        <div class="note-content">{note['text']}</div>
        <div class="note-timestamp">{note['timestamp']}</div>
    </li>'''
    print(f"DEBUG: Returning HTML response (status 200)")
    return html_response

@app.route('/notes')
def get_notes():
    """Get all notes as HTML fragment (for testing purposes)."""
    if not notes:
        return '<li class="no-notes">No notes yet. Add one above!</li>'

    html_parts = []
    for note in notes:
        html_parts.append(f'''<li class="note-item">
            <div class="note-content">{note['text']}</div>
            <div class="note-timestamp">{note['timestamp']}</div>
        </li>''')

    return '\n'.join(html_parts)

@app.route('/clear', methods=['POST'])
def clear_notes():
    """Clear all notes (for testing purposes)."""
    global notes
    notes.clear()
    return '<li class="no-notes">All notes cleared!</li>'

@app.after_request
def add_security_headers(response):
    """Add security headers for production use."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
