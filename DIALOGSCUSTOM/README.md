# DIALOGSCUSTOM - Custom Modal Dialogs with HTMX

This example demonstrates how to build custom modal dialogs from scratch using HTMX and Hyperscript, without relying on CSS frameworks like Bootstrap or UIKit.

## 🎯 Overview

The DIALOGSCUSTOM example shows how to create fully customizable modal dialogs with smooth animations, event-driven behavior, and clean separation of concerns. This approach gives you complete control over styling and functionality.

## 🚀 Features

- **No Framework Dependencies**: Built from scratch without Bootstrap, UIKit, or other CSS frameworks
- **HTMX Dynamic Loading**: Modal content loaded from server on demand
- **Hyperscript Events**: Clean, declarative event handling for modal lifecycle
- **Custom Animations**: Smooth fade-in/fade-out and zoom effects using CSS keyframes
- **Click-to-Close**: Click outside modal (on underlay) to dismiss
- **Event-Driven**: Uses Hyperscript's `closeModal` custom event
- **Fully Responsive**: Mobile-friendly design with responsive breakpoints
- **Security Headers**: CSP and security headers for production use

## 🛠️ HTMX Patterns

- `hx-get="/modal"` - Load modal content from server
- `hx-target="body"` - Target the body element
- `hx-swap="beforeend"` - Append content to end of body

## 🎨 Hyperscript Features

- `_="on closeModal..."` - Event listener for custom closeModal event
- `add .closing` - Add CSS class to trigger close animation
- `wait for animationend` - Wait for animation to complete before removal
- `then remove me` - Remove modal from DOM after animation
- `on click trigger closeModal` - Trigger custom event on click

## 📁 File Structure

```
DIALOGSCUSTOM/
├── myapp.py                 # Flask application
├── templates/
│   ├── index.html          # Main page with modal trigger
│   └── modal.html          # Modal content template
├── static/
│   ├── css/
│   │   └── style.css       # Custom styles with animations
│   └── img/
│       ├── favicon.svg     # Favicon
│       └── favicon-emoji.svg
├── myapp_test.py           # Unit tests (20 tests)
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── DESIGN.md               # Design decisions
```

## 🏃♂️ Running the Example

1. **Install dependencies**:
   ```bash
   cd DIALOGSCUSTOM
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
- Hyperscript integration
- Modal content structure
- Event handlers and animations
- Security headers

## 🔧 How It Works

1. **Button Click**: User clicks "Open a Modal" button
2. **HTMX Request**: HTMX sends `GET` request to `/modal`
3. **Server Response**: Flask returns modal HTML fragment
4. **Append to Body**: HTMX appends modal to end of `<body>` using `beforeend`
5. **Animations**: CSS animations create smooth fade-in and zoom effects
6. **User Interaction**: User can:
   - Click outside modal (underlay) to close
   - Click "Close" button to trigger close
7. **Close Animation**: Hyperscript:
   - Listens for `closeModal` event
   - Adds `.closing` class for exit animation
   - Waits for `animationend` event
   - Removes modal from DOM

## 🎨 Customization

### Styling
The example includes comprehensive custom CSS in `static/css/style.css`:
- Modal positioning and layout
- Fade-in/fade-out animations
- Zoom-in/zoom-out animations
- Responsive design
- Custom button styles
- Gradient backgrounds

### Animations
Modify keyframe animations in CSS:
```css
@keyframes fadeIn {
    0% { opacity: 0; }
    100% { opacity: 1; }
}
```

### Content
Modify `templates/modal.html` to customize modal content:
- Add forms, inputs, or complex layouts
- Include images, videos, or dynamic content
- Add multiple buttons or actions

## 🔒 Security

The application includes security headers:
- Content Security Policy (CSP) allowing Hyperscript and HTMX
- X-Content-Type-Options
- X-Frame-Options
- X-XSS-Protection
- Strict-Transport-Security

## 📚 Related Examples

- **DIALOGSBROWSER**: Native browser dialogs with `hx-prompt` and `hx-confirm`
- **DIALOGSUIKIT**: UIKit framework modal dialogs
- **DIALOGSBOOTSTRAP**: Bootstrap framework modal dialogs

## 🌐 Based On

This example is based on the official HTMX custom modal example:
https://htmx.org/examples/modal-custom/

## 📝 License

This example is part of the HTMX Flask Examples project and follows the same licensing terms.

