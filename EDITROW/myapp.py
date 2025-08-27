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
"""

from flask import Flask, render_template, request
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
    """Return read-only contact row."""
    contact = next((c for c in CONTACTS if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404

    # Return read-only row HTML fragment with HTMX attributes
    return f'''
<!-- hx-target="closest tr": Update this row -->
<!-- hx-swap="outerHTML": Replace entire row with server response -->
<tr>
    <td>{contact['name']}</td>
    <td>{contact['email']}</td>
    <td>
        <!-- hx-get="/contact/{contact['id']}/edit": Load edit form -->
        <!-- hx-trigger="edit": Trigger on custom 'edit' event -->
        <button class="btn primary"
                hx-get="/contact/{contact['id']}/edit"
                hx-trigger="edit"
                onclick="let editing = document.querySelector('.editing');
                         if(editing) {{
                             if(confirm('Already editing! Cancel and continue?')) {{
                                 htmx.trigger(editing, 'cancel');
                                 htmx.trigger(this, 'edit');
                             }}
                         }} else {{
                             htmx.trigger(this, 'edit');
                         }}">
            Edit
        </button>
    </td>
</tr>
'''


@app.route('/contact/<int:contact_id>/edit')
def edit_contact(contact_id):
    """Return edit form for a specific contact."""
    contact = next((c for c in CONTACTS if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404

    # Return edit form HTML fragment with HTMX attributes
    return f'''
<!-- hx-trigger="cancel": Respond to cancel event -->
<!-- hx-get="/contact/{contact['id']}": Load original row when cancelled -->
<tr hx-trigger="cancel" class="editing" hx-get="/contact/{contact['id']}">
    <td><input autofocus name="name" value="{contact['name']}"></td>
    <td><input name="email" value="{contact['email']}"></td>
    <td>
        <!-- hx-get="/contact/{contact['id']}": Cancel edit and return to read-only view -->
        <button class="btn secondary" hx-get="/contact/{contact['id']}">
            Cancel
        </button>
        <!-- hx-put="/contact/{contact['id']}": Submit updated data -->
        <!-- hx-include="closest tr": Include all form inputs from this row -->
        <button class="btn primary"
                hx-put="/contact/{contact['id']}"
                hx-include="closest tr">
            Save
        </button>
    </td>
</tr>
'''


@app.route('/contact/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update a contact by ID."""
    global CONTACTS

    contact = next((c for c in CONTACTS if c['id'] == contact_id), None)
    if not contact:
        return "Contact not found", 404

    # Update contact data from form
    contact['name'] = request.form.get('name', contact['name'])
    contact['email'] = request.form.get('email', contact['email'])

    # Return updated read-only row HTML fragment
    return f'''
<!-- hx-target="closest tr": Update this row -->
<!-- hx-swap="outerHTML": Replace entire row with server response -->
<tr>
    <td>{contact['name']}</td>
    <td>{contact['email']}</td>
    <td>
        <!-- hx-get="/contact/{contact['id']}/edit": Load edit form -->
        <!-- hx-trigger="edit": Trigger on custom 'edit' event -->
        <button class="btn primary"
                hx-get="/contact/{contact['id']}/edit"
                hx-trigger="edit"
                onclick="let editing = document.querySelector('.editing');
                         if(editing) {{
                             if(confirm('Already editing a row! Cancel that edit and continue?')) {{
                                 htmx.trigger(editing, 'cancel');
                                 htmx.trigger(this, 'edit');
                             }}
                         }} else {{
                             htmx.trigger(this, 'edit');
                         }}">
            Edit
        </button>
    </td>
</tr>
'''


if __name__ == '__main__':
    app.run(debug=True)
