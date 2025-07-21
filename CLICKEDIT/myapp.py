#!/usr/bin/env python3
"""
HTMX Click-to-Edit Example

This example demonstrates inline editing using HTMX patterns:
- hx-get: Load edit form
- hx-put: Submit edited content
- hx-target: Update specific elements
- hx-swap: Control how content is replaced

Based on the official HTMX click-to-edit example.
"""

from flask import Flask, render_template, request
app = Flask(__name__)

# Sample contact data
CONTACT = {
    "firstName": "Manny",
    "lastName": "Pacquiao",
    "email": "manny@pacquiao.com"
}


@app.route('/')
def index():
    """Main page with contact display."""
    return render_template('index.html')


@app.route('/contact/edit')
def edit_contact():
    """Return edit form for the contact."""
    # Return edit form HTML fragment with HTMX attributes for inline editing
    return f'''
<!-- hx-put="/contact/update": Submit form data to update endpoint -->
<!-- hx-target="this": Update this form element -->
<!-- hx-swap="outerHTML": Replace entire form with server response -->
<form hx-put="/contact/update" hx-target="this" hx-swap="outerHTML">
  <div>
    <label>First Name</label>
    <input type="text" name="firstName" value="{CONTACT['firstName']}">
  </div>
  <div class="form-group">
    <label>Last Name</label>
    <input type="text" name="lastName" value="{CONTACT['lastName']}">
  </div>
  <div class="form-group">
    <label>Email Address</label>
    <input type="email" name="email" value="{CONTACT['email']}">
  </div>
  <button class="btn" type="submit">Submit</button>
  <!-- hx-get="/contact/cancel": Load original display without changes -->
  <button class="btn" hx-get="/contact/cancel">Cancel</button>
</form>
'''


@app.route('/contact/update', methods=['PUT'])
def update_contact():
    """Update contact information."""
    # Update contact data from form
    CONTACT["firstName"] = request.form.get("firstName", CONTACT["firstName"])
    CONTACT["lastName"] = request.form.get("lastName", CONTACT["lastName"])
    CONTACT["email"] = request.form.get("email", CONTACT["email"])

    # Return updated contact display HTML fragment with HTMX attributes
    return f'''
<!-- hx-target="this": Update this display element -->
<!-- hx-swap="outerHTML": Replace entire display with server response -->
<div hx-target="this" hx-swap="outerHTML">
    <div><label>First Name</label>: {CONTACT['firstName']}</div>
    <div><label>Last Name</label>: {CONTACT['lastName']}</div>
    <div><label>Email</label>: {CONTACT['email']}</div>
    <!-- hx-get="/contact/edit": Load edit form when button is clicked -->
    <button hx-get="/contact/edit" class="btn primary">
        Click To Edit
    </button>
</div>
'''


@app.route('/contact/cancel')
def cancel_edit():
    """Cancel editing and return to display view."""
    # Return contact display HTML fragment (unchanged) with HTMX attributes
    return f'''
<!-- hx-target="this": Update this display element -->
<!-- hx-swap="outerHTML": Replace entire display with server response -->
<div hx-target="this" hx-swap="outerHTML">
    <div><label>First Name</label>: {CONTACT['firstName']}</div>
    <div><label>Last Name</label>: {CONTACT['lastName']}</div>
    <div><label>Email</label>: {CONTACT['email']}</div>
    <!-- hx-get="/contact/edit": Load edit form when button is clicked -->
    <button hx-get="/contact/edit" class="btn primary">
        Click To Edit
    </button>
</div>
'''


if __name__ == '__main__':
    app.run(debug=True)
