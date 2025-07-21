# HTMX Click-to-Edit Example

A demonstration of inline editing using HTMX patterns. This example shows how to implement click-to-edit functionality for a single contact, allowing users to edit contact information directly in the page without page refreshes.

**Based on the official HTMX click-to-edit example at: https://htmx.org/examples/click-to-edit/**

## 🎯 Learning Objectives

This example demonstrates:
- **Inline editing** with `hx-get` and `hx-put`
- **Targeted updates** using `hx-target` and `hx-swap`
- **Form handling** with HTMX form submission
- **Progressive enhancement** without JavaScript frameworks

## 👤 User Story

As a user, I want to edit contact information inline without page refreshes so that I can quickly update data with immediate feedback and a seamless editing experience.

## 🔄 How It Works

1. **Initial Display**: Page loads showing contact information with "Click To Edit" button
2. **Edit Mode**: User clicks "Click To Edit" button
   - HTMX sends GET request to `/contact/edit`
   - Server returns edit form HTML fragment
   - HTMX replaces display with form using `hx-swap="outerHTML"`
3. **Data Entry**: User modifies contact fields (firstName, lastName, email)
4. **Submit Changes**: User clicks "Submit" button
   - HTMX sends PUT request to `/contact/update` with form data
   - Server updates contact data and returns updated display HTML
   - HTMX replaces form with updated display
5. **Cancel Option**: User can click "Cancel" to restore original display without changes

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Run the Application**:
   ```bash
   uv run myapp.py
   ```

3. **Access the Example**:
   Open your browser to `http://localhost:5000`

4. **Run Tests**:
   ```bash
   uv run myapp_test.py
   ```

## Code Structure

```
CLICKEDIT/
├── myapp.py              # Flask application with contact editing logic
├── myapp_test.py         # Unit tests for the implementation
├── templates/
│   └── index.html        # Main interface with single contact display
├── static/
│   └── css/
│       └── style.css     # Contact display and form styling
├── pyproject.toml        # Project dependencies
├── DESIGN.md             # Detailed design documentation
└── README.md             # This file
```

## API Endpoints

- `GET /`: Main page with contact display
- `GET /contact/edit`: Returns edit form for the contact
- `PUT /contact/update`: Updates contact information
- `GET /contact/cancel`: Cancels editing and returns to display

## Implementation Details

### Flask Routes

- **`/` (GET)**: Serves the main page with contact display
- **`/contact/edit` (GET)**: Returns edit form HTML for the contact
- **`/contact/update` (PUT)**: Updates contact data and returns updated display
- **`/contact/cancel` (GET)**: Returns display view (for cancel functionality)

### HTMX Integration

The implementation uses several key HTMX patterns:

1. **Click to Edit**: Uses `hx-get="/contact/edit"` to load edit form
2. **Form Submission**: Uses `hx-put="/contact/update"` to update data
3. **Targeted Updates**: Uses `hx-target="this"` and `hx-swap="outerHTML"`
4. **Inline Replacement**: Form replaces the display seamlessly
5. **Cancel Function**: Uses `hx-get="/contact/cancel"` to restore display

### Data Management

- Uses in-memory single contact for simplicity
- Contact has: firstName, lastName, and email
- Updates are applied immediately to the data structure
- No database persistence (for educational purposes)

## Testing

The implementation includes comprehensive unit tests that verify:
- Contact display and rendering
- Edit form loading and structure
- Contact data updates
- Cancel functionality
- HTML structure validation
- CSS class presence

Run tests with:
```bash
uv run myapp_test.py
```

## Customization

### Adding New Contact Fields
To add new fields (e.g., phone number):

1. Update the `CONTACT` data structure in `myapp.py`
2. Add form fields to the edit form HTML in `edit_contact()` function
3. Update the `update_contact()` function to handle new fields
4. Update the display HTML in both `update_contact()` and `cancel_edit()` functions

### Changing Contact Data
Modify the `CONTACT` dictionary in `myapp.py`:
```python
CONTACT = {
    "firstName": "Manny",
    "lastName": "Pacquiao",
    "email": "manny@pacquiao.com"
}
```

### Styling Customization
The CSS uses CSS custom properties for easy theming:
```css
:root {
    --primary-color: #007bff;    /* Change main color */
    --secondary-color: #6c757d;  /* Change secondary color */
    --success-color: #28a745;    /* Change success color */
}
```

## HTMX Patterns Demonstrated

### Core Attributes
- **`hx-get`**: Load edit form when button is clicked
- **`hx-put`**: Submit form data to update endpoint
- **`hx-target`**: Specify which element to update
- **`hx-swap`**: Control how content is replaced

### User Experience
- **Seamless editing**: No page refreshes required
- **Immediate feedback**: Changes appear instantly
- **Cancel functionality**: Users can cancel edits
- **Accessible**: Proper form labels and semantic HTML

## Browser Compatibility

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Requires JavaScript enabled for HTMX functionality
- Graceful degradation (forms work without HTMX)

## Dependencies

- **Flask**: Web framework for server-side logic
- **HTMX**: Client-side library for dynamic interactions
- **Python 3.8+**: Required for modern Python features

## Related Examples

This example complements other HTMX patterns:
- **ACTIVESEARCH**: Live search with debouncing
- **VALUESELECT**: Cascading dropdowns
- **PLY3**: Mutually exclusive form elements
- **PROGRESSBAR**: Real-time progress updates

---

**Note**: This is an educational example. For production use, consider adding:
- Database persistence
- Input validation
- CSRF protection
- User authentication
- Error logging