#!/usr/bin/env python3
"""
HTMX Bulk Update Example

This example demonstrates bulk operations using HTMX patterns:
- hx-post: Send POST request with form data for bulk updates
- hx-target: Target specific elements for response updates
- hx-swap: Control how content is replaced with timing
- Form handling: Process multiple checkbox selections
- Toast notifications: User feedback for bulk operations

Based on the official HTMX bulk-update example.
Follows Development Guiding Light principles for educational clarity.
"""

from flask import Flask, render_template, request, jsonify
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sample contact data with Filipino boxers and status
CONTACTS = [
    {"id": 1, "name": "Manny Pacquiao",
     "email": "manny@pacquiao.com", "status": "Active"},
    {"id": 2, "name": "Nonito Donaire",
     "email": "nonito@donaire.com", "status": "Active"},
    {"id": 3, "name": "Donnie Nietes",
     "email": "donnie@nietes.com", "status": "Inactive"},
    {"id": 4, "name": "Jerwin Ancajas",
     "email": "jerwin@ancajas.com", "status": "Active"},
    {"id": 5, "name": "John Riel Casimero",
     "email": "john@casimero.com", "status": "Inactive"},
    {"id": 6, "name": "Mark Magsayo",
     "email": "mark@magsayo.com", "status": "Active"},
    {"id": 7, "name": "Rey Vargas",
     "email": "rey@vargas.com", "status": "Inactive"},
    {"id": 8, "name": "Emanuel Navarrete",
     "email": "emanuel@navarrete.com", "status": "Active"},
    {"id": 9, "name": "Luis Nery",
     "email": "luis@nery.com", "status": "Active"},
    {"id": 10, "name": "Brandon Figueroa",
     "email": "brandon@figueroa.com", "status": "Inactive"},
]


@app.route('/')
def index():
    """Main page with contact table and bulk update form."""
    return render_template('index.html', contacts=CONTACTS)


@app.route('/bulk-update', methods=['POST'])
def bulk_update():
    """Process bulk update request with checkbox selections.

    This function demonstrates inline HTML generation for simple, repetitive
    fragments following the Development Guiding Light principle of using inline
    HTML for simple feedback rather than complex template systems.
    """
    global CONTACTS

    # Get form data from the bulk update request
    form_data = request.form

    # Process checkbox selections for status updates
    # Demonstrates efficient server-side processing of form data
    updated_count = 0
    for key, value in form_data.items():
        if key.startswith('status:'):
            # Extract email from checkbox name (status:email@domain)
            # This naming convention allows easy parsing and identification
            email = key.split(':', 1)[1]

            # Find and update the contact
            for contact in CONTACTS:
                if contact['email'] == email:
                    # Update status based on checkbox value
                    # 'on' means checked (Active), empty string means
                    # unchecked (Inactive)
                    contact['status'] = 'Active' if value == 'on'\
                                                 else 'Inactive'
                    updated_count += 1
                    break

    # Generate toast notification HTML fragment
    # This demonstrates inline HTML generation for simple, repetitive fragments
    # Following the Development Guiding Light principle of avoiding complex
    # templates for simple feedback messages
    toast_html = f'''
<!-- Toast notification for bulk update results -->
<!-- hx-target="#toast": Update the toast element -->
<!-- hx-swap="innerHTML settle:3s": Replace content with 3-second settling -->
<div id="toast" class="toast success" role="alert" aria-live="polite">
    <div class="toast-content">
        <span class="toast-icon">✓</span>
        <div class="toast-message">
            <strong>Bulk Update Complete!</strong><br>
            Updated {updated_count} contact(s) successfully.
        </div>
    </div>
    <button class="toast-close" onclick="this.parentElement.remove()"
            aria-label="Close notification">
        ×
    </button>
</div>'''

    return toast_html


@app.route('/api/contacts')
def api_contacts():
    """API endpoint to get all contacts (for potential future enhancements)."""
    return jsonify(CONTACTS)


@app.route('/api/contacts/count')
def api_contacts_count():
    """API endpoint to get contact count and status breakdown."""
    active_count = sum(1 for c in CONTACTS if c['status'] == 'Active')
    inactive_count = len(CONTACTS) - active_count

    return jsonify({
        "total": len(CONTACTS),
        "active": active_count,
        "inactive": inactive_count
    })


if __name__ == '__main__':
    app.run(debug=True)
