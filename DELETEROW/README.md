# HTMX Delete Row Example

A Flask application demonstrating row deletion with confirmation and fade-out animation using HTMX.

## Overview

This example shows how to implement a delete button that removes a table row upon completion, with a confirmation dialog and smooth fade-out animation. It's based on the [official HTMX delete-row example](https://htmx.org/examples/delete-row/).

## Features

- **Confirmation Dialog**: Shows "Are you sure?" before deletion
- **Fade-out Animation**: Smooth 1-second fade-out before row removal
- **Server-side Deletion**: Proper DELETE requests to remove data
- **Responsive Design**: Clean, modern UI with hover effects

## User Story

As a user managing a contact list, I want to delete contacts with a confirmation step and visual feedback, so that I can safely remove entries without accidental deletions and see the row smoothly disappear.

## How It Works

1. **Initial Load**: The page displays a table of Filipino boxer contacts
2. **Delete Action**: Clicking a "Delete" button triggers the deletion process
3. **Confirmation**: A browser confirmation dialog appears asking "Are you sure?"
4. **Server Request**: If confirmed, HTMX sends a DELETE request to `/contact/{id}`
5. **Fade-out**: The row fades out over 1 second using CSS transitions
6. **Removal**: After the animation, the row is completely removed from the DOM

## HTMX Patterns Used

- **`hx-delete`**: Sends DELETE request to remove the contact
- **`hx-confirm`**: Shows confirmation dialog before action
- **`hx-target="closest tr"`**: Targets the closest table row to the button
- **`hx-swap="outerHTML swap:1s"`**: Replaces entire row with 1-second delay for animation

## Installation & Usage

1. **Install dependencies**:
   ```bash
   uv pip install flask
   ```

2. **Run the application**:
   ```bash
   uv run myapp.py
   ```

3. **Open your browser** and navigate to `http://localhost:5000`

4. **Test the functionality**:
   - Click any "Delete" button
   - Confirm the deletion in the dialog
   - Watch the row fade out and disappear

## Customization

### Changing the Confirmation Message
Modify the `hx-confirm` attribute in `templates/index.html`:
```html
<tbody hx-confirm="Your custom message here?" hx-target="closest tr" hx-swap="outerHTML swap:1s">
```

### Adjusting Animation Duration
Change the `swap:1s` in the `hx-swap` attribute and update the CSS transition:
```html
<tbody hx-confirm="Are you sure?" hx-target="closest tr" hx-swap="outerHTML swap:2s">
```

```css
tr.htmx-swapping td {
    opacity: 0;
    transition: opacity 2s ease-out;  /* Match the swap duration */
}
```

### Adding Different Animation Effects
Modify the CSS in `static/css/style.css`:
```css
tr.htmx-swapping td {
    opacity: 0;
    transform: translateX(-100px);  /* Slide out to the left */
    transition: opacity 1s ease-out, transform 1s ease-out;
}
```

## File Structure

```
DELETEROW/
├── myapp.py              # Flask application with delete logic
├── templates/
│   └── index.html        # Main template with HTMX attributes
├── static/
│   └── css/
│       └── style.css     # Styles including fade-out animation
├── myapp_test.py         # Unit tests
├── pyproject.toml        # Project configuration
└── README.md            # This file
```

## Testing

Run the unit tests:
```bash
uv run myapp_test.py
```

## Related Examples

- [Click-to-Edit](../CLICKEDIT/): Inline editing functionality
- [Click-to-Load](../CLICKLOAD/): Lazy loading with pagination
- [Active Search](../ACTIVESEARCH/): Live search functionality
