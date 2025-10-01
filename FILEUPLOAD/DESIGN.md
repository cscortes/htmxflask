# File Upload - Design Document

## Overview

This example demonstrates HTMX file upload with real-time progress tracking, following the official HTMX pattern from [htmx.org/examples/file-upload](https://htmx.org/examples/file-upload/).

## Core Design Decisions

### 1. Inline HTML Responses (Not JSON)

**Decision**: Flask routes return HTML snippets directly, not JSON.

**Rationale**:
- Follows HTMX philosophy of "HTML over the wire"
- Simpler code - no client-side rendering logic needed
- More educational - clear data flow from server to browser
- Matches official HTMX examples

**Implementation**:
```python
# Success response
return '<div class="success">✅ Successfully uploaded file.pdf</div>'

# Error response
return '<div class="error">❌ File too large</div>', 400
```

### 2. Single Template File

**Decision**: Only `index.html` template; responses are inline HTML.

**Rationale**:
- Reduces file count and complexity
- Easier to understand for learners
- Better performance (no template rendering overhead)
- Follows Development Guiding Light principle of minimal files

**Alternative Considered**: Separate templates for each response type
- **Rejected**: Adds complexity without educational benefit

### 3. Real Progress Tracking with JavaScript

**Decision**: Use JavaScript to listen to `htmx:xhr:progress` events.

**Rationale**:
- HTMX provides progress data but cannot update progress bars directly
- This is the official HTMX pattern for file uploads
- JavaScript is minimal (~20 lines) and well-documented
- No alternative pure-HTMX solution exists for real progress

**Implementation**:
```javascript
htmx.on('#upload-form', 'htmx:xhr:progress', function(evt) {
    var percent = (evt.detail.loaded / evt.detail.total) * 100;
    htmx.find('#progress').setAttribute('value', percent);
});
```

### 4. Original Filenames (Not Unique)

**Decision**: Save files with their original names (sanitized).

**Rationale**:
- Simpler code - no UUID generation needed
- Easier to identify uploaded files
- More transparent behavior
- Matches educational focus

**Tradeoff**: Files with same name will overwrite. This is acceptable for an educational example.

### 5. Server-Side Validation

**Decision**: Comprehensive validation before saving files.

**Security Checks**:
- File extension validation
- File size limits (16MB)
- Empty file rejection
- Path traversal prevention (via `secure_filename()`)
- Invalid character filtering

**Implementation**:
```python
def validate_file(file):
    """Validate uploaded file for security and constraints."""
    # Extension check
    # Size check
    # Security check
    return {'valid': True/False, 'error': 'message'}
```

## Architecture Choices

### Response Flow

```
User selects file
    ↓
Clicks Upload
    ↓
HTMX sends POST with multipart/form-data
    ↓
JavaScript tracks progress via htmx:xhr:progress
    ↓
Progress bar updates in real-time
    ↓
Server validates and saves file
    ↓
Returns HTML snippet (success/error)
    ↓
HTMX swaps response into target div
    ↓
Custom event triggers file list refresh
```

### File Storage

- **Location**: `uploads/` directory
- **Security**: `secure_filename()` prevents path traversal
- **Naming**: Original filename (sanitized)
- **Persistence**: Files remain until manually deleted

## Performance Considerations

### Optimizations
- **Inline HTML**: No template rendering overhead for responses
- **Minimal CSS**: 96 lines, loads instantly
- **No bundling**: Direct file serving
- **Efficient validation**: Early returns on validation failures

### Acceptable for Educational Example
- **No chunked uploads**: Simple single-request pattern
- **No resumable uploads**: Demonstrates core concept clearly
- **In-memory processing**: Flask handles file buffering

## Accessibility

- Standard HTML form elements (native accessibility)
- Progress bars have implicit ARIA roles
- Error messages visible and screen-reader friendly
- Keyboard navigation works naturally

## Browser Compatibility

- **Modern browsers**: Chrome, Firefox, Safari, Edge
- **Requirements**:
  - `<progress>` element support
  - XHR progress events
  - No IE support needed

## Alternatives Considered

### 1. Template-Based Responses
- **Rejected**: Adds complexity, more files to maintain
- **Current**: Inline HTML in routes

### 2. Unique Filenames with UUIDs
- **Rejected**: Over-engineering for educational example
- **Current**: Original filenames (sanitized)

### 3. Fake Progress Indicators
- **Rejected**: Not educational, misleading
- **Current**: Real progress via `htmx:xhr:progress`

### 4. Drag-and-Drop Interface
- **Rejected**: Adds JavaScript complexity beyond HTMX scope
- **Current**: Simple file input (standard HTML)

### 5. Client-Side Validation
- **Rejected**: Server-side validation is mandatory anyway
- **Current**: Server-side only (simpler, more secure)

## Development Guiding Light Compliance

✅ **One Example Per Feature**: Focuses on file upload with progress
✅ **Minimal Dependencies**: Only HTMX and Flask
✅ **Vanilla HTML**: Standard form elements
✅ **Flask-First**: Simple routes with inline HTML
✅ **Educational Structure**: Clear, commented, easy to understand
✅ **Minimal CSS**: 96 lines of focused styling
✅ **Justified JavaScript**: ~20 lines for progress tracking (explained why needed)
✅ **Inline HTML for fragments**: Simple responses don't need templates

## Testing Strategy

**Note**: Traditional unit tests removed in favor of manual testing for this educational example.

**Manual Test Checklist**:
1. Upload single file - verify progress bar works
2. Upload multiple files - verify all upload
3. Upload invalid type - verify error message
4. Upload oversized file - verify rejection
5. View file list - verify files appear
6. Delete file - verify removal
7. Upload same filename twice - verify overwrite

## Future Enhancements (Not Implemented)

These are intentionally NOT included to keep the example focused:
- Chunked uploads for large files
- Resumable uploads
- Image preview/thumbnails
- Drag-and-drop interface
- Client-side validation
- File type icons from libraries
- Advanced error recovery

---

**Last Updated**: 2025-10-01
**Based on**: https://htmx.org/examples/file-upload/
