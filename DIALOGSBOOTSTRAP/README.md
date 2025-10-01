# DIALOGSBOOTSTRAP - Bootstrap Modal Dialogs with HTMX

This example demonstrates how to integrate HTMX with Bootstrap's native modal dialog functionality, creating dynamic modal content that loads from the server.

## 🎯 Overview

The DIALOGSBOOTSTRAP example shows how to combine HTMX's dynamic content loading with Bootstrap's robust modal system. This approach leverages the best of both worlds: HTMX's simplicity for server communication and Bootstrap's polished UI components.

## 🚀 Features

- **Bootstrap Modal Integration**: Uses Bootstrap 5's native modal functionality
- **HTMX Dynamic Loading**: Modal content loaded dynamically from server
- **Responsive Design**: Mobile-friendly modal dialogs
- **Backdrop Blur Effect**: Enhanced visual appeal with backdrop blur
- **Accessibility**: Proper ARIA attributes and keyboard navigation
- **Security Headers**: CSP and security headers for production use

## 🛠️ HTMX Patterns

- `hx-get="/modal"` - Load modal content from server
- `hx-target="#modals-here"` - Target the modal container
- `hx-trigger="click"` - Trigger on button click

## 🎨 Bootstrap Features

- `data-bs-toggle="modal"` - Bootstrap modal trigger
- `data-bs-target="#modals-here"` - Modal target container
- `modal-lg modal-dialog-centered` - Responsive centered modal
- `modal-blur` - Custom backdrop blur effect

## 📁 File Structure

```
DIALOGSBOOTSTRAP/
├── myapp.py                 # Flask application
├── templates/
│   ├── index.html          # Main page with modal trigger
│   └── modal.html          # Modal content template
├── static/
│   ├── css/
│   │   └── style.css       # Custom styling
│   └── img/
│       ├── favicon.svg     # Favicon
│       └── favicon-emoji.svg
├── myapp_test.py           # Unit tests
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── DESIGN.md               # Design decisions
```

## 🏃♂️ Running the Example

1. **Install dependencies**:
   ```bash
   cd DIALOGSBOOTSTRAP
   uv pip install -e .
   ```

2. **Run the application**:
   ```bash
   python myapp.py
   ```

3. **Open in browser**:
   Navigate to `http://localhost:5000`

## 🧪 Testing

Run the comprehensive test suite:

```bash
python myapp_test.py
```

The test suite includes 20 test cases covering:
- Page loading and HTMX attributes
- Bootstrap modal functionality
- Modal content structure
- Security headers
- Accessibility features

## 🔧 How It Works

1. **Button Click**: User clicks the "Open Bootstrap Modal" button
2. **Dual Trigger**: Both HTMX (`hx-get`) and Bootstrap (`data-bs-toggle`) are triggered
3. **Bootstrap Shows Modal**: Bootstrap immediately shows the modal container
4. **HTMX Loads Content**: HTMX sends a `GET` request to `/modal` and loads content into `.modal-content`
5. **Server Response**: Flask returns the modal content (header, body, footer)
6. **User Interaction**: User can interact with modal and close it using Bootstrap's native close functionality

## 🎨 Customization

### Styling
The example includes minimal custom CSS in `static/css/style.css`:
- Enhanced modal backdrop blur
- Custom button hover effects
- Responsive design adjustments

### Content
Modify `templates/modal.html` to customize modal content:
- Add forms, inputs, or complex layouts
- Include additional Bootstrap components
- Add HTMX attributes for form submissions

## 🔒 Security

The application includes security headers:
- Content Security Policy (CSP)
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security

## 📚 Related Examples

- **DIALOGSBROWSER**: Native browser dialogs with `hx-prompt` and `hx-confirm`
- **DIALOGSUIKIT**: UIKit framework modal dialogs
- **FILEUPLOAD**: File upload with modal feedback

## 🌐 Based On

This example is based on the official HTMX Bootstrap modal example:
https://htmx.org/examples/modal-bootstrap/

## 📝 License

This example is part of the HTMX Flask Examples project and follows the same licensing terms.
