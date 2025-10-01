# HTMX + Flask Best Practices

**Simplified File Upload Pattern**

This document provides best practices for building HTMX file upload applications with Flask, following the official HTMX pattern from [htmx.org/examples/file-upload](https://htmx.org/examples/file-upload/).

---

## Table of Contents

1. [The Simplified Pattern](#the-simplified-pattern)
2. [Form Submission with HTMX](#form-submission-with-htmx)
3. [Real Progress Tracking](#real-progress-tracking)
4. [Response Format](#response-format)
5. [Route Configuration](#route-configuration)
6. [Security Best Practices](#security-best-practices)
7. [Common Pitfalls](#common-pitfalls)

---

## The Simplified Pattern

### ✅ Official HTMX File Upload Pattern

Follow the official HTMX example for clean, maintainable code:

**HTML (index.html):**
```html
<form id="upload-form"
      hx-encoding="multipart/form-data"
      hx-post="/upload"
      hx-target="#upload-result">

    <input type="file" name="file">
    <button type="submit">Upload</button>
    <progress id="progress" value="0" max="100"></progress>
</form>

<div id="upload-result"></div>

<script>
    // Track real upload progress
    htmx.on('#upload-form', 'htmx:xhr:progress', function(evt) {
        htmx.find('#progress').setAttribute('value',
            evt.detail.loaded/evt.detail.total * 100
        );
    });
</script>
```

**Python (myapp.py):**
```python
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '<div class="error">❌ No file provided</div>', 400

    file = request.files['file']

    # Validation...

    file.save(file_path)

    return f'''<div class="success">
        ✅ Successfully uploaded <strong>{filename}</strong>
    </div>'''
```

**Key Principles:**
- ✅ Return HTML snippets, not JSON
- ✅ Use one main template (index.html)
- ✅ Real progress tracking with `htmx:xhr:progress`
- ✅ Simple, educational code structure

---

## Form Submission with HTMX

### ❌ DON'T: Mix Browser and HTMX Attributes

```html
<!-- BAD: Conflicting attributes -->
<form method="post" enctype="multipart/form-data"
      hx-post="/upload" hx-encoding="multipart/form-data">
```

**Problem:** Browser and HTMX both try to handle submission.

### ✅ DO: Use HTMX Attributes Only

```html
<!-- GOOD: Let HTMX handle everything -->
<form hx-post="/upload"
      hx-encoding="multipart/form-data"
      hx-target="#result">
```

**Why:** HTMX needs exclusive control for async uploads.

---

## Real Progress Tracking

### ✅ Use htmx:xhr:progress Event

The official HTMX pattern uses the `htmx:xhr:progress` event for real progress:

```javascript
htmx.on('#upload-form', 'htmx:xhr:progress', function(evt) {
    // evt.detail.loaded = bytes uploaded so far
    // evt.detail.total = total bytes to upload
    var percent = (evt.detail.loaded / evt.detail.total) * 100;
    htmx.find('#progress').setAttribute('value', percent);
});
```

### ❌ DON'T: Use Fake Progress Indicators

```css
/* BAD: Fake indicator that doesn't show real progress */
.htmx-request .upload-progress {
    display: block;  /* Just shows/hides, no real progress */
}
```

### ✅ DO: Use HTML5 Progress Element

```html
<!-- GOOD: Real progress bar -->
<progress id="progress" value="0" max="100"></progress>
```

With CSS:
```css
progress {
    width: 100%;
    height: 20px;
}

progress::-webkit-progress-value {
    background-color: #3b82f6;
    transition: width 0.3s ease;
}
```

---

## Response Format

### ✅ Return HTML Snippets

Keep it simple - return HTML directly from Flask:

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    # Success
    return f'''<div class="success">
        ✅ Successfully uploaded <strong>{filename}</strong> ({size} KB)
    </div>'''

    # Error
    return f'<div class="error">❌ {error_message}</div>', 400
```

### ❌ DON'T: Use Separate Templates for Responses

```python
# BAD: Unnecessary complexity
return render_template('upload_result.html',
                       success=True,
                       filename=filename)
```

**Why Inline HTML is Better:**
- ✅ Simpler code
- ✅ Less files to maintain
- ✅ More educational
- ✅ Follows HTMX philosophy

---

## Route Configuration

### ✅ Single Route, Clear Purpose

```python
@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload."""
    # Single, focused handler
```

### ❌ DON'T: Create Conflicting Routes

```python
# BAD: Multiple handlers for same path
@app.route('/upload', methods=['OPTIONS'])
def handle_cors():
    pass

@app.route('/upload', methods=['POST'])
def upload():
    pass
```

**Problem:** Flask can't decide which to use → 405 Method Not Allowed

### ✅ Use @app.after_request for Headers

```python
@app.after_request
def add_security_headers(response):
    """Add headers to all responses."""
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
```

---

## Security Best Practices

### File Validation

```python
def validate_file(file):
    """Validate uploaded file."""
    filename = file.filename

    # 1. Check extension
    if '.' not in filename:
        return {'valid': False, 'error': 'No extension'}

    extension = filename.rsplit('.', 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return {'valid': False, 'error': f'Type .{extension} not allowed'}

    # 2. Check size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_SIZE:
        return {'valid': False, 'error': 'File too large'}

    if size == 0:
        return {'valid': False, 'error': 'File is empty'}

    # 3. Check for path traversal
    invalid_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\', '..']
    if any(char in filename for char in invalid_chars):
        return {'valid': False, 'error': 'Invalid filename'}

    return {'valid': True}
```

### Secure Filename Handling

```python
from werkzeug.utils import secure_filename
import uuid

# Generate unique, safe filename
original = secure_filename(file.filename)
extension = Path(original).suffix
unique_filename = f"{uuid.uuid4()}{extension}"
```

### Size Limits

```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

@app.errorhandler(RequestEntityTooLarge)
def handle_too_large(error):
    return '<div class="error">❌ File too large (max 16MB)</div>', 413
```

---

## Common Pitfalls

### 1. ❌ Expecting JSON When Returning HTML

```python
# BAD: Tests expect JSON
response_data = response.get_json()
self.assertTrue(response_data['success'])
```

```python
# GOOD: Parse HTML instead
html = response.get_data(as_text=True)
self.assertIn('Successfully uploaded', html)
```

### 2. ❌ Auto-Submit on File Selection

```javascript
// BAD: Submits immediately when file selected
fileInput.addEventListener('change', () => {
    form.submit();
});
```

**Problem:** User can't review their selection.

```javascript
// GOOD: Let user click Upload button
// No auto-submit code needed!
```

### 3. ❌ Not Verifying File Save

```python
# BAD: Assume save worked
file.save(file_path)
return success_response()
```

```python
# GOOD: Verify file was saved
file.save(file_path)
if not os.path.exists(file_path):
    return '<div class="error">Save failed</div>', 500
return success_response()
```

### 4. ❌ Complex Directory Structures

```
templates/
├── index.html
├── upload_result.html          ❌ Unnecessary
├── multi_upload_result.html    ❌ Unnecessary
├── file_list.html              ❌ Unnecessary
```

```
templates/
└── index.html                  ✅ Simple!
```

**Use inline HTML in routes instead of separate templates.**

---

## Golden Rules

1. **Follow Official Examples** - HTMX documentation shows the right way
2. **Keep It Simple** - One template, inline responses, clear code
3. **Return HTML, Not JSON** - Embrace HTMX's HTML-over-the-wire philosophy
4. **Real Progress Tracking** - Use `htmx:xhr:progress` for actual upload progress
5. **Validate Everything** - Server-side validation is mandatory
6. **Test with HTML** - Parse HTML responses in tests, not JSON
7. **One Route, One Purpose** - Don't create conflicting route handlers

---

## Quick Reference

### Minimal File Upload Example

**HTML:**
```html
<form hx-post="/upload" hx-encoding="multipart/form-data" hx-target="#result">
    <input type="file" name="file">
    <button>Upload</button>
    <progress id="progress" value="0" max="100"></progress>
</form>
<div id="result"></div>

<script>
htmx.on('form', 'htmx:xhr:progress', (e) => {
    document.getElementById('progress').value = e.detail.loaded/e.detail.total*100;
});
</script>
```

**Python:**
```python
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save(f'uploads/{secure_filename(file.filename)}')
    return '<div class="success">✅ Uploaded!</div>'
```

That's it! Simple, clear, and educational. 🚀

---

**Last Updated:** 2025-10-01 (Simplified following official HTMX pattern)
