# HTMX Click-to-Load Example

**Version**: 0.7.3

A demonstration of lazy loading content using HTMX patterns.
This example shows how to implement progressive loading of data
without page refreshes, based on the
[official HTMX click-to-load example]
(https://htmx.org/examples/click-to-load/).

## 🎯 User Story

**As a user**, I want to browse through a large list of contacts
without waiting for all data to load at once, so that I can see
content quickly and load more as needed.

## 🚀 Quick Start

```bash
# Install dependencies
uv sync

# Run the application
uv run myapp.py

# Visit http://localhost:5000
```

## 🔧 How It Works

This example demonstrates the click-to-load pattern
with the following workflow:

1. **Initial Load**: Page displays first 3 contacts with a "Load More" button
2. **User Interaction**: User clicks "Load More Contacts..." button
3. **HTMX Request**: `hx-get="/contacts/?page=2"` sends request to server
4. **Server Response**: Returns HTML fragment with next 3 contacts
5. **DOM Update**: `hx-target="#replaceMe"` and `hx-swap="outerHTML"`
replace the button row with new content
6. **Progressive Loading**: Process continues until all contacts are loaded

## 🎨 HTMX Features Demonstrated

### Core Attributes
- **`hx-get`**: Load additional content from server endpoint
- **`hx-target`**: Specify which element to update (`#replaceMe`)
- **`hx-swap`**: Control how content is replaced (`outerHTML`)

### Advanced Features
- **Pagination**: Load 3 contacts per page
- **Loading Indicators**: Show "Loading..." during requests
- **Progressive Enhancement**: Works without JavaScript (graceful degradation)
- **Fragment Responses**: Server returns HTML fragments, not full pages

## 📋 API Endpoints

| Endpoint | Method | Description | Response |
|----------|--------|-------------|----------|
| `/` | GET | Main page with initial contacts | Full HTML page |
| `/contacts/` | GET | Load additional contacts | HTML fragment |

### Query Parameters
- `page`: Page number to load (default: 1)

### Response Format
Returns HTML content based on request type:
- **Full page**: Complete HTML with head, body, and table structure
- **Fragment**: HTML fragments containing contact rows and load more button
- **End state**: "All contacts loaded" message when complete

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
uv run python myapp_test.py

# Expected output: 9 tests passing
```

### Test Coverage
- ✅ Page loading and initial content
- ✅ Pagination functionality (pages 1-8)
- ✅ HTMX attribute validation
- ✅ HTML structure verification
- ✅ CSS class name validation
- ✅ Edge cases (beyond last page)

## 🎨 Customization

### Data Source
Modify the `CONTACTS` list in `myapp.py` to use your own data:

```python
CONTACTS = [
    {"id": 1, "name": "Your Name", "email": "your@email.com",
    "status": "Active"},
    # Add more contacts...
]
```

**Current Dataset**: 24 Filipino boxers and athletes across 8 pages

### Pagination Size
Change `ITEMS_PER_PAGE` to adjust how many items load per request:

```python
ITEMS_PER_PAGE = 5  # Load 5 items at a time
```

### Styling
Customize the appearance by modifying `static/css/style.css`:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
}
```

## 🔍 Technical Details

### Server-Side Logic
- **Pagination**: Calculates start/end indices based on page number
- **Unified Template**: Single template handles both full page and fragment
 responses
- **State Management**: Tracks current page and remaining data

### Client-Side Behavior
- **Progressive Loading**: Loads content incrementally
- **Loading States**: Shows indicators during requests
- **DOM Manipulation**: Replaces specific elements without full page refresh

### Performance Benefits
- **Reduced Initial Load**: Only loads visible content
- **Bandwidth Efficiency**: Transfers only needed data
- **Better UX**: Faster perceived performance

## 📚 Learning Resources

- [Official HTMX Click-to-Load Example]
(https://htmx.org/examples/click-to-load/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contributing

This example follows the [Development Guiding Light]
(../docs/DEVGUIDINGLIGHT.md) principles:
- Minimal dependencies (Flask + HTMX only)
- Educational code with clear comments
- Comprehensive testing
- Standard HTML (no HTML5-specific elements)
- Clean, maintainable structure

## 📄 License

This example is part of the HTMX Flask Examples project. See [LICENSE]
(../LICENSE) for details.