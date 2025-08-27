# Edit Row Example

## HTMX Features Demonstrated

- **Primary**: `hx-get`, `hx-put`, `hx-target="closest tr"`
- **Secondary**: `hx-swap="outerHTML"`, `hx-trigger="edit"`, `hx-include="closest tr"`

## User Story

As a user, I want to edit table rows inline so that I can quickly update data without navigating to a separate edit page.

## How It Works

1. User clicks "Edit" button on any table row
2. HTMX sends GET request to `/contact/{id}/edit`
3. Server returns HTML fragment with input fields
4. HTMX replaces the row with the edit form
5. User modifies data and clicks "Save"
6. HTMX sends PUT request with form data
7. Server updates the contact and returns read-only row
8. HTMX replaces the edit form with updated data

## Key Features

- **Single Row Editing**: Only one row can be edited at a time
- **Inline Editing**: No page navigation required
- **Form Data Handling**: Uses `hx-include="closest tr"` to collect input data
- **Cancel Functionality**: Users can cancel edits and return to read-only view
- **Visual Feedback**: Editing rows are highlighted with special styling

## HTMX Patterns Used

### Row Targeting
```html
<tbody hx-target="closest tr" hx-swap="outerHTML">
```
All requests from within the table target the closest table row and replace the entire row.

### Custom Event Triggers
```html
<button hx-get="/contact/1/edit" hx-trigger="edit">
```
Uses custom `edit` event instead of default click to allow JavaScript integration.

### Form Data Inclusion
```html
<button hx-put="/contact/1" hx-include="closest tr">
```
Includes all form inputs from the closest table row when submitting.

### Cancel Event Handling
```html
<tr hx-trigger="cancel" class="editing" hx-get="/contact/1">
```
Row responds to `cancel` event to return to read-only state.

## JavaScript Integration

The example includes minimal JavaScript to prevent multiple rows from being edited simultaneously:

```javascript
let editing = document.querySelector('.editing');
if(editing) {
    if(confirm('Already editing! Cancel and continue?')) {
        htmx.trigger(editing, 'cancel');
        htmx.trigger(this, 'edit');
    }
} else {
    htmx.trigger(this, 'edit');
}
```

## Try It Out

1. `cd EDITROW`
2. `uv sync`
3. `uv run myapp.py`
4. Visit http://localhost:5000

## Learning Points

- Demonstrates complex HTMX interactions with custom events
- Shows how to handle form data without traditional forms
- Example of JavaScript integration for enhanced UX
- Pattern for single-instance editing in tables
- Server-side HTML generation for dynamic content

## Based On

This example is based on the official HTMX [Edit Row example](https://htmx.org/examples/edit-row/).
