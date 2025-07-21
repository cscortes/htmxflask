#!/usr/bin/env python3
"""
HTMX Click-to-Load Example

This example demonstrates lazy loading using HTMX patterns:
- hx-get: Load additional content on demand
- hx-target: Update specific elements
- hx-swap: Control how content is replaced
- Pagination: Load more items incrementally

Based on the official HTMX click-to-load example.
"""

from flask import Flask, render_template, request
app = Flask(__name__)

# Sample contact data with pagination
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
    {"id": 11, "name": "Stephen Fulton", "email": "stephen@fulton.com",
     "status": "Active"},
    {"id": 12, "name": "Naoya Inoue", "email": "naoya@inoue.com",
     "status": "Active"},
    {"id": 13, "name": "Pedro Taduran", "email": "pedro@taduran.com",
     "status": "Active"},
    {"id": 14, "name": "Rene Cuarto", "email": "rene@cuarto.com",
     "status": "Active"},
    {"id": 15, "name": "Carl Jammes Martin", "email": "carl@martin.com",
     "status": "Active"},
    {"id": 16, "name": "Vincent Astrolabio", "email": "vincent@astrolabio.com",
     "status": "Active"},
    {"id": 17, "name": "Dave Apolinario", "email": "dave@apolinario.com",
     "status": "Active"},
    {"id": 18, "name": "Melvin Jerusalem", "email": "melvin@jerusalem.com",
     "status": "Active"},
    {"id": 19, "name": "Regie Suganob", "email": "regie@suganob.com",
     "status": "Active"},
    {"id": 20, "name": "ArAr Andales", "email": "arar@andales.com",
     "status": "Active"},
    {"id": 21, "name": "Carlo Paalam", "email": "carlo@paalam.com",
     "status": "Active"},
    {"id": 22, "name": "Nesthy Petecio", "email": "nesthy@petecio.com",
     "status": "Active"},
    {"id": 23, "name": "Eumir Marcial", "email": "eumir@marcial.com",
     "status": "Active"},
    {"id": 24, "name": "Irish Magno", "email": "irish@magno.com",
     "status": "Active"},
]

ITEMS_PER_PAGE = 3


@app.route('/')
def index():
    """Main page with initial contact list."""
    # Get first page of contacts
    page = 1
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    contacts = CONTACTS[start_idx:end_idx]

    # Use the main template for full page rendering
    return render_template('index.html',
                           contacts=contacts, page=page,
                           has_more=end_idx < len(CONTACTS))


@app.route('/contacts/')
def load_contacts():
    """Load additional contacts for pagination."""
    page = int(request.args.get('page', 1))
    start_idx = (page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    contacts = CONTACTS[start_idx:end_idx]
    has_more = end_idx < len(CONTACTS)

    # Generate HTML fragment inline for HTMX partial updates
    html_parts = []

    # Add contact rows
    for contact in contacts:
        html_parts.append(f'''<tr>
    <td>{contact['id']}</td>
    <td>{contact['name']}</td>
    <td>{contact['email']}</td>
    <td class="status-{contact['status'].lower()}">{contact['status']}</td>
</tr>''')

    # Add load more button or end message
    if has_more:
        html_parts.append(f'''<!-- hx-target="this": Update this row -->
<!-- hx-swap="outerHTML": Replace entire row with server response -->
<tr id="replaceMe">
    <td colspan="4">
        <!-- hx-get="/contacts/?page={page + 1}": Load next page -->
        <button class="btn primary" hx-get="/contacts/?page={page + 1}"
                hx-target="#replaceMe" hx-swap="outerHTML">
            Load More Contacts...
            <span class="htmx-indicator">Loading...</span>
        </button>
    </td>
</tr>''')
    else:
        html_parts.append('''<tr>
    <td colspan="4" class="no-more">
        <em>All contacts loaded!</em>
    </td>
</tr>''')

    return '\n'.join(html_parts)


if __name__ == '__main__':
    app.run(debug=True)
