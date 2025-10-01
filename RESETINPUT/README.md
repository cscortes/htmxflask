# Reset User Input - HTMX Example

## HTMX Features Demonstrated

- **Primary**: `hx-on::after-request` - Execute JavaScript after HTMX request completes
- **Secondary**: `hx-post`, `hx-target`, `hx-swap="afterbegin"`, `hx-include`, `hx-confirm`

## User Story

As a user adding notes, I want the input field to automatically clear after successfully adding a note, so I can quickly add multiple notes without manually clearing the field each time.

## How It Works

1. User types a note and clicks "Add Note"
2. HTMX sends POST request to `/note` endpoint
3. Server validates input and creates new note with timestamp
4. Server returns HTML fragment for the new note
5. HTMX inserts the new note at the top of the list (`hx-swap="afterbegin"`)
6. `hx-on::after-request` executes JavaScript to reset the form
7. Input field is cleared automatically for the next note

## Key HTMX Patterns

### Method 1: Form Reset
```html
<form hx-post="/note"
      hx-target="#notes"
      hx-swap="afterbegin"
      hx-on::after-request="if(event.detail.successful) this.reset()">
    <input type="text" name="note-text" placeholder="Enter your note here...">
    <button type="submit">Add Note</button>
</form>
```

### Method 2: Individual Input Reset
```html
<input id="note-input" type="text" name="note-text" placeholder="Enter your note here...">
<button hx-post="/note"
        hx-target="#notes"
        hx-swap="afterbegin"
        hx-include="#note-input"
        hx-on::after-request="if(event.detail.successful) document.getElementById('note-input').value = ''">
    Add Note
</button>
```

## Learning Points

- **`hx-on::after-request`**: Execute JavaScript after HTMX request completes
- **`event.detail.successful`**: Check if request was successful (2xx status)
- **`this.reset()`**: Reset entire form to initial state (form elements only)
- **`hx-swap="afterbegin"`**: Prepend new content to target element
- **`hx-include`**: Include specific elements in form data when not using a form
- **`hx-confirm`**: Show confirmation dialog before executing request

## Try It Out

1. `cd RESETINPUT`
2. `uv sync`
3. `uv run myapp.py`
4. Visit http://localhost:5000
5. Add notes and watch the input field automatically clear!

## Debugging the Reset Functionality

To see the reset functionality in action and debug any issues:

1. **Open Developer Tools** (F12) and go to the **Console** tab
2. **Type a note** and click "Add Note"
3. **Watch the console** for these messages:
   ```
   HTMX Request completed: {successful: true, xhr: 200, statusText: 'OK'}
   Request was successful, form should reset
   Resetting form via this.reset()
   ```
4. **Expected behavior**: Input field should clear automatically
5. **If reset doesn't work**: Check for JavaScript errors in console

The example includes comprehensive debugging with console logging to help you understand what's happening behind the scenes.

## Testing

Run the comprehensive test suite:
```bash
python myapp_test.py
```

Tests cover:
- Form submission and note creation
- HTML fragment responses
- Error handling for empty notes
- Multiple note management
- HTMX attribute validation
- Security headers
- Both reset methods demonstration

## Troubleshooting

### Common Issue: `htmx:evalDisallowedError`

If you see `htmx:evalDisallowedError` in the browser console, this means HTMX is blocking the execution of JavaScript code in attributes due to security settings.

**Cause**: The HTMX configuration has `htmx.config.allowEval = false` which prevents inline JavaScript execution in `hx-on::*` attributes.

**Solution**: Use event listeners instead of inline JavaScript:

```html
<!-- ❌ Problematic (causes evalDisallowedError) -->
<form hx-on::after-request="if(event.detail.successful) this.reset()">

<!-- ✅ Fixed (uses event listeners) -->
<form id="form-reset-method" hx-post="/note" hx-target="#notes" hx-swap="afterbegin">
```

**JavaScript Event Listener**:
```javascript
document.body.addEventListener('htmx:afterRequest', function(evt) {
    if (evt.detail.successful && evt.target.id === 'form-reset-method') {
        evt.target.reset();
    }
});
```

**Benefits of Event Listener Approach**:
- Works with `allowEval = false` security setting
- Cleaner HTML without inline JavaScript
- Better debugging and maintainability
- Proper separation of concerns

## Based On

This example is based on the official HTMX example: https://htmx.org/examples/reset-user-input/
