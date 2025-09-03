#!/usr/bin/env python3
"""
HTMX Edit Row Example

This example demonstrates editable table rows using HTMX patterns:
- hx-get: Load edit form for a specific row
- hx-put: Submit edited row data  
- hx-target: Target the closest table row for updates
- hx-swap: Control how content is replaced
- hx-trigger: Custom event handling for edit/cancel
- hx-include: Include form data from closest row

Based on the official HTMX edit-row example.
Follows Development Guiding Light principles for educational clarity.
"""

from flask import Flask, render_template, request, jsonify
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sample contact data with Filipino boxers
CONTACTS = [
    {"id": 1, "name": "Manny Pacquiao", "email": "manny@pacquiao.com"},
    {"id": 2, "name": "Nonito Donaire", "email": "nonito@donaire.com"},
    {"id": 3, "name": "Donnie Nietes", "email": "donnie@nietes.com"},
    {"id": 4, "name": "Jerwin Ancajas", "email": "jerwin@ancajas.com"},
    {"id": 5, "name": "John Riel Casimero", "email": "john@casimero.com"},
]


@app.route('/')
def index():
    """Main page with contact table."""
    return render_template('index.html', contacts=CONTACTS)


@app.route('/contact/<int:contact_id>')
def get_contact(contact_id):
    """Return read-only contact row with comprehensive HTMX comments."""
    contact = next((c for c in CONTACTS if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404

    # Generate read-only row HTML fragment with detailed HTMX comments
    # This demonstrates inline HTML generation for simple, repetitive fragments
    html_fragment = f'''
<!-- hx-target="closest tr": Update this specific table row -->
<!-- hx-swap="outerHTML": Replace entire row with server response -->
<tr>
    <td>{contact['name']}</td>
    <td>{contact['email']}</td>
    <td>
        <!-- hx-get: Load edit form for this contact -->
        <!-- hx-trigger="edit": Trigger on custom 'edit' event -->
        <!-- hx-target="closest tr": Target this row for the edit form -->
        <button class="btn primary"
                hx-get="/contact/{contact['id']}/edit"
                hx-trigger="edit"
                hx-target="closest tr"
                data-contact-id="{contact['id']}">
            Edit
        </button>
    </td>
</tr>'''
    
    return html_fragment


@app.route('/contact/<int:contact_id>/edit')
def edit_contact(contact_id):
    """Return edit form for a specific contact with enhanced HTMX attributes."""
    contact = next((c for c in CONTACTS if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404

    # Generate edit form HTML fragment with comprehensive HTMX comments
    # Demonstrates form handling and event management
    html_fragment = f'''
<!-- hx-trigger="cancel": Respond to cancel event -->
<!-- hx-get: Load original row when cancelled -->
<!-- hx-target="closest tr": Target this row for updates -->
<!-- hx-swap="outerHTML": Replace entire row with server response -->
<tr hx-trigger="cancel" 
    hx-get="/contact/{contact['id']}"
    hx-target="closest tr"
    hx-swap="outerHTML"
    class="editing" 
    data-contact-id="{contact['id']}">
    
    <!-- Form inputs with proper labels and validation -->
    <td>
        <input type="text" 
               name="name" 
               value="{contact['name']}" 
               autofocus
               required
               aria-label="Contact name">
    </td>
    <td>
        <input type="email" 
               name="email" 
               value="{contact['email']}" 
               required
               aria-label="Contact email">
    </td>
    <td>
        <!-- Cancel button: Return to read-only view -->
        <!-- hx-get: Load original contact data -->
        <!-- hx-target: Update this row -->
        <button class="btn secondary" 
                hx-get="/contact/{contact['id']}"
                hx-target="closest tr"
                hx-swap="outerHTML">
            Cancel
        </button>
        
        <!-- Save button: Submit updated data -->
        <!-- hx-put: Use PUT method for updates (RESTful) -->
        <!-- hx-include="closest tr": Include all form inputs from this row -->
        <!-- hx-target="closest tr": Update this row with response -->
        <button class="btn primary"
                hx-put="/contact/{contact['id']}"
                hx-include="closest tr"
                hx-target="closest tr"
                hx-swap="outerHTML">
            Save
        </button>
    </td>
</tr>'''
    
    return html_fragment


@app.route('/contact/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update a contact by ID with validation and error handling."""
    global CONTACTS

    contact = next((c for c in CONTACTS if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404

    # Get and validate form data
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    
    # Basic validation
    if not name or not email:
        return "Name and email are required", 400
    
    if '@' not in email:
        return "Invalid email format", 400

    # Update contact data
    contact['name'] = name
    contact['email'] = email

    # Return updated read-only row HTML fragment
    # Demonstrates successful update with visual feedback
    html_fragment = f'''
<!-- hx-target="closest tr": Update this row -->
<!-- hx-swap="outerHTML": Replace entire row with server response -->
<tr class="updated-row">
    <td>{contact['name']}</td>
    <td>{contact['email']}</td>
    <td>
        <!-- hx-get: Load edit form for this contact -->
        <!-- hx-trigger="edit": Trigger on custom 'edit' event -->
        <!-- hx-target="closest tr": Target this row for updates -->
        <button class="btn primary"
                hx-get="/contact/{contact['id']}/edit"
                hx-trigger="edit"
                hx-target="closest tr"
                data-contact-id="{contact['id']}">
            Edit
        </button>
    </td>
</tr>'''
    
    return html_fragment


@app.route('/api/contacts')
def api_contacts():
    """API endpoint to get all contacts (for potential future enhancements)."""
    return jsonify(CONTACTS)


if __name__ == '__main__':
    app.run(debug=True)
