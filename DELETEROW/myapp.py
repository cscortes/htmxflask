#!/usr/bin/env python3
"""
HTMX Delete Row Example

This example demonstrates row deletion using HTMX patterns:
- hx-delete: Send DELETE request to remove row
- hx-confirm: Show confirmation dialog before deletion
- hx-target: Target the closest table row for removal
- hx-swap: Control how content is replaced with fade-out animation

Based on the official HTMX delete-row example.
Follows Development Guiding Light principles for educational clarity.
"""

from flask import Flask, render_template, jsonify
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sample contact data with Filipino boxers
CONTACTS = [
    {"id": 1, "name": "Manny Pacquiao", "email": "manny@pacquiao.com",
     "status": "Active"},
    {"id": 2, "name": "Nonito Donaire", "email": "nonito@donaire.com",
     "status": "Active"},
    {"id": 3, "name": "Donnie Nietes", "email": "donnie@nietes.com",
     "status": "Active"},
    {"id": 4, "name": "Jerwin Ancajas", "email": "jerwin@ancajas.com",
     "status": "Active"},
    {"id": 5, "name": "John Riel Casimero", "email": "john@casimero.com",
     "status": "Active"},
    {"id": 6, "name": "Mark Magsayo", "email": "mark@magsayo.com",
     "status": "Active"},
    {"id": 7, "name": "Rey Vargas", "email": "rey@vargas.com",
     "status": "Inactive"},
    {"id": 8, "name": "Emanuel Navarrete", "email": "emanuel@navarrete.com",
     "status": "Active"},
    {"id": 9, "name": "Luis Nery", "email": "luis@nery.com",
     "status": "Active"},
    {"id": 10, "name": "Brandon Figueroa", "email": "brandon@figueroa.com",
     "status": "Active"},
]


@app.route('/')
def index():
    """Main page with contact table."""
    return render_template('index.html', contacts=CONTACTS)


@app.route('/contact/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete a contact by ID with validation and error handling."""
    global CONTACTS

    # Find the contact to be deleted
    contact_to_delete = next((c for c in CONTACTS if c['id'] == contact_id), None)

    if not contact_to_delete:
        # Return error response if contact not found
        return "Contact not found", 404

    # Remove the contact from the list
    CONTACTS = [contact for contact in CONTACTS if contact['id'] != contact_id]

    # Return empty response - HTMX will remove the row
    # hx-swap="outerHTML swap:1s" handles the fade-out animation
    # This demonstrates how HTMX handles empty responses gracefully
    return ''


@app.route('/api/contacts')
def api_contacts():
    """API endpoint to get all contacts (for potential future enhancements)."""
    return jsonify(CONTACTS)


@app.route('/api/contacts/count')
def api_contacts_count():
    """API endpoint to get contact count (useful for UI updates)."""
    return jsonify({"count": len(CONTACTS)})


if __name__ == '__main__':
    app.run(debug=True)
