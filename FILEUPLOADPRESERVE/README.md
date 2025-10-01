# File Upload Input Preservation

**HTMX Example**: Demonstrates preserving file inputs after form validation errors using the `hx-preserve` attribute.

Based on: [HTMX File Upload Input Preservation Example](https://htmx.org/examples/file-upload-input/)

## 🎯 HTMX Features Demonstrated

- **`hx-preserve`**: Preserves file input values after form errors
- **`hx-post`**: Handles form submission via AJAX
- **`hx-target`**: Targets specific elements for content replacement
- **`hx-swap`**: Controls how content is replaced
- **Form validation**: Server-side validation with error handling
- **File upload**: Multipart form data handling

## 📖 User Story

> As a user uploading files with additional form data, I want my file selection to be preserved when validation errors occur, so I don't have to re-select the file after fixing form errors.

## 🔧 How It Works

### The Problem
When using server-side validation with forms that include file inputs, the file input's value is lost when the form returns with error messages. Users must re-upload their files, creating a poor user experience.

### The Solution: hx-preserve
The `hx-preserve` attribute tells HTMX to preserve the element's value when the form is updated after an error:

```html
<input type="file" name="file" hx-preserve>
```

### Alternative Approach: Form Restructuring
You can also preserve file inputs by moving them outside the form element:

```html
<input form="myForm" type="file" name="file">
<form id="myForm" hx-target="#myForm" hx-swap="outerHTML">
    <!-- other form fields -->
    <button type="submit">Submit</button>
</form>
```

## 🚀 Try It Out

1. **Start the server**:
   ```bash
   cd FILEUPLOADPRESERVE
   python myapp.py
   ```

2. **Open your browser** to `http://localhost:5007`

3. **Test the examples**:
   - **With hx-preserve**: Fill out the form with invalid data and submit. Notice the file selection is preserved.
   - **Without hx-preserve**: Do the same with the second form. Notice the file selection is lost.

## 📚 Learning Points

### HTMX Attributes Used
- **`hx-preserve`**: Preserves element values during HTMX updates
- **`hx-post`**: Sends POST request to specified URL
- **`hx-target`**: Specifies which element to update with response
- **`hx-swap`**: Controls how the target element is updated

### Form Validation
- **Client-side**: HTML5 validation attributes (`required`, `type="email"`)
- **Server-side**: Python validation with error messages
- **File validation**: Extension checking and size limits

### Error Handling
- **Validation errors**: Displayed inline with form fields
- **File errors**: Specific messages for file-related issues
- **Server errors**: Graceful error handling with user feedback

## 🔒 Security Features

- **File type validation**: Only allowed extensions accepted
- **File size limits**: 16MB maximum file size
- **Filename sanitization**: Prevents path traversal attacks
- **Security headers**: XSS protection and content type validation
- **Input validation**: Server-side validation of all form fields

## 🧪 Testing

Run the comprehensive test suite:

```bash
python myapp_test.py
```

**Test Coverage**:
- ✅ Form validation (name, email, file)
- ✅ File upload success scenarios
- ✅ Error handling and validation messages
- ✅ hx-preserve functionality
- ✅ Security features (file sanitization, headers)
- ✅ Edge cases (no file, invalid types, large files)

## 📁 File Structure

```
FILEUPLOADPRESERVE/
├── myapp.py                 # Flask application
├── myapp_test.py           # Unit tests
├── templates/
│   ├── index.html          # Main page with two examples
│   ├── form_with_errors.html           # Error form with hx-preserve
│   └── form_with_errors_no_preserve.html # Error form without hx-preserve
├── static/
│   ├── css/
│   │   └── style.css       # Styling for forms and errors
│   └── img/
│       ├── favicon.svg     # Primary favicon
│       └── favicon-emoji.svg # Fallback favicon
├── uploads/                # Directory for uploaded files
├── README.md              # This file
└── DESIGN.md              # Design decisions and architecture
```

## 🌐 Browser Compatibility

- **Modern browsers**: Chrome, Firefox, Safari, Edge
- **HTMX support**: Requires HTMX 1.9+ (uses 2.0.6)
- **File API**: Uses HTML5 File API for file selection
- **Form validation**: HTML5 validation with fallbacks

## 🔗 Related Examples

- [File Upload](../FILEUPLOAD/) - Basic file upload with progress
- [Inline Validation](../INLINVALIDATION/) - Real-time form validation
- [Form Submission](../ACTIVESEARCH/) - Form handling patterns

## 📖 Further Reading

- [HTMX hx-preserve Documentation](https://htmx.org/attributes/hx-preserve/)
- [HTMX File Upload Input Preservation Example](https://htmx.org/examples/file-upload-input/)
- [HTML5 Form Validation](https://developer.mozilla.org/en-US/docs/Web/HTML/Constraint_validation)
- [Flask File Uploads](https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/)
