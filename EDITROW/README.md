# EDITROW Example

## HTMX Features Demonstrated

**Primary**: `hx-get`, `hx-put`, `hx-target="closest tr"`, `hx-swap="outerHTML"`
**Secondary**: `hx-trigger="edit"`, `hx-include="closest tr"`, custom event handling

## User Story

As a user, I want to edit contact information directly in a table row so that I can quickly update data without navigating to a separate page or form.

## How It Works

1. **Initial State**: Table displays contacts in read-only format with edit buttons
2. **Edit Mode**: User clicks edit button → HTMX loads edit form inline
3. **Form Display**: Row transforms into editable inputs with save/cancel buttons
4. **Data Update**: User modifies data and clicks save → HTMX sends PUT request
5. **Row Update**: Server validates data and returns updated read-only row
6. **Single Instance**: Only one row can be edited at a time (JavaScript managed)

## HTMX Patterns Explained

### Core Attributes
- **`hx-get="/contact/{id}/edit"`**: Loads edit form for specific contact
- **`hx-put="/contact/{id}"`**: Submits updated data using RESTful PUT method
- **`hx-target="closest tr"`**: Targets the table row containing the button
- **`hx-swap="outerHTML"`**: Replaces entire row with server response

### Advanced Features
- **`hx-trigger="edit"`**: Custom event trigger for edit mode
- **`hx-include="closest tr"`**: Includes all form inputs when submitting
- **`hx-trigger="cancel"`**: Responds to cancel events from JavaScript

### JavaScript Integration
- **Single-instance editing**: Prevents multiple rows from being edited
- **User confirmation**: Asks before canceling current edit
- **Visual feedback**: Success styling for updated rows
- **Focus management**: Automatically focuses edit inputs

## Try It Out

1. `cd EDITROW`
2. `uv sync`
3. `uv run myapp.py`
4. Visit http://localhost:5000

## Learning Points

### HTMX Best Practices
- **Row-level targeting**: Use `closest tr` for precise table row updates
- **Form data inclusion**: `hx-include="closest tr"` captures all inputs
- **Custom events**: `hx-trigger="edit"` enables complex interaction patterns
- **RESTful methods**: PUT for updates, GET for data retrieval

### Server-Side Patterns
- **Inline HTML generation**: Generate HTML fragments directly in Python
- **Validation**: Server-side data validation before updates
- **Error handling**: Proper HTTP status codes and error messages
- **State management**: Global data structure with proper updates

### User Experience
- **Immediate feedback**: Visual indicators for editing state
- **Confirmation dialogs**: Prevent accidental data loss
- **Responsive design**: Mobile-friendly table and form elements
- **Accessibility**: ARIA labels, semantic HTML, keyboard navigation

## Code Structure

```
EDITROW/
├── myapp.py              # Flask routes with inline HTML generation
├── templates/
│   └── index.html        # Main template with HTMX attributes
├── static/
│   ├── css/
│   │   └── style.css     # Responsive styling with CSS custom properties
│   └── js/
│       └── editrow.js    # Minimal JavaScript for single-instance editing
└── README.md             # This documentation
```

## Technical Implementation

### Flask Routes
- **`/`**: Main page with contact table
- **`/contact/<id>`**: Get read-only contact row
- **`/contact/<id>/edit`**: Get edit form for contact
- **`/contact/<id>` (PUT)**: Update contact data
- **`/api/contacts`**: JSON endpoint for future enhancements

### Data Flow
1. **Template Rendering**: Jinja2 renders initial table with contacts
2. **HTMX Request**: Edit button triggers GET request for edit form
3. **Server Response**: Flask returns HTML fragment with form inputs
4. **Form Submission**: Save button triggers PUT request with form data
5. **Data Update**: Server validates and updates contact data
6. **Row Refresh**: Updated read-only row replaces edit form

### Error Handling
- **Validation**: Required fields and email format checking
- **HTTP Status**: Proper 400/404 responses for errors
- **User Feedback**: Clear error messages and visual indicators

## Browser Compatibility

- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **HTMX Version**: 2.0.3 (latest stable)
- **CSS Features**: CSS Grid, Flexbox, Custom Properties
- **JavaScript**: ES6+ features with fallbacks

## Performance Considerations

- **Minimal JavaScript**: Only essential functionality beyond HTMX
- **Efficient Targeting**: `closest tr` for precise DOM updates
- **Inline HTML**: Reduces template overhead for simple fragments
- **CSS Optimization**: Custom properties for consistent theming

## Accessibility Features

- **Semantic HTML**: Proper table structure with `<th>` and `<td>`
- **ARIA Labels**: Descriptive labels for form inputs
- **Keyboard Navigation**: Focus management and keyboard shortcuts
- **Screen Reader Support**: Proper heading hierarchy and table roles
- **High Contrast**: Support for high contrast mode preferences
- **Reduced Motion**: Respects user motion preferences

## Future Enhancements

- **Real-time validation**: Server-side field validation with immediate feedback
- **Bulk operations**: Select multiple rows for batch updates
- **Search/filtering**: Add contact search and filtering capabilities
- **Data persistence**: Database integration for persistent storage
- **User authentication**: Add user management and access control

---

**Note**: This example follows the Development Guiding Light principles, demonstrating how to build complex interactions with minimal JavaScript while maintaining excellent user experience and educational value.
