# Development Guiding Light 🌟

This document serves as the **north star** for developing HTMX examples in this repository. Every implementation decision should align with these core principles to ensure consistency, simplicity, and educational value.

## 🎯 Core Philosophy

**"Hypermedia-first, JavaScript-last"** - Demonstrate the power of HTMX to build modern web interactions with minimal JavaScript while maintaining excellent user experience.

## 📋 Development Principles

### 1. **One Example Per HTMX Feature**
- Each example demonstrates **one primary HTMX concept**
- Focus on clarity over complexity
- Avoid feature mixing that could confuse learners
- If multiple features are needed, clearly document the primary vs. supporting features

**✅ Good**: Click-to-Edit example focuses on `hx-get` and `hx-swap`  
**❌ Bad**: Click-to-Edit that also includes file upload, validation, and real-time updates

### 2. **Minimal External Dependencies**
- **No external JavaScript libraries** unless absolutely necessary for the core HTMX feature
- Prefer native browser APIs over third-party solutions
- Only exception: Libraries that directly enhance HTMX (like HTMX extensions)

**✅ Allowed**: HTMX core library, HTMX extensions, Flask-SocketIO for WebSocket examples  
**❌ Avoid**: jQuery, React, Vue, Alpine.js, Chart.js, etc.

### 3. **Vanilla HTML + Minimal Enhancements**
- Use standard HTML elements as the foundation
- Progressive enhancement approach
- HTMX attributes should feel natural on standard HTML elements
- Minimal CSS for basic styling and layout

**✅ Example**:
```html
<button hx-get="/api/data" hx-target="#result">Load Data</button>
<div id="result"></div>
```

### 4. **Flask-First Server Architecture**
- Keep Flask routes simple and focused
- Use Jinja2 templates for server-side rendering
- Demonstrate server-side thinking vs. client-side complexity
- Each example should work without JavaScript (graceful degradation)

### 5. **Educational Code Structure**
- **Self-documenting**: Code should be readable without extensive comments
- **Commented HTMX attributes**: Explain what each `hx-*` attribute does
- **Clear naming**: Routes, templates, and variables should be descriptive
- **Minimal abstractions**: Avoid over-engineering for the sake of DRY

**✅ Example**:
```html
<!-- hx-post: Send form data to server -->
<!-- hx-target: Replace content in #result div -->
<!-- hx-indicator: Show loading spinner while request is active -->
<form hx-post="/submit" hx-target="#result" hx-indicator="#spinner">
    <input type="text" name="message" placeholder="Enter message">
    <button type="submit">Send</button>
</form>
<div id="spinner" class="htmx-indicator">Loading...</div>
<div id="result"></div>
```

## 🏗️ Implementation Standards

### File Organization
```
example-name/
├── myapp.py          # Flask routes and logic
├── templates/
│   ├── index.html    # Main page template
│   └── fragments/    # HTMX partial templates
├── static/
│   ├── css/
│   │   └── style.css # Minimal styling
│   └── js/
│       └── htmx.js   # HTMX library
└── Pipfile          # Dependencies
```

### Naming Conventions
- **Routes**: `/example-name/`, `/example-name/action`
- **Templates**: `example-name.html`, `fragment-name.html`
- **CSS Classes**: `.htmx-indicator`, `.example-container`, `.form-group`
- **IDs**: `#target-area`, `#form-container`, `#result-section`

### HTML Structure
- Use standard HTML elements (`<div>`, `<form>`, `<table>`, etc.) - avoid HTML5-specific elements
- HTMX attributes should be the last attributes on elements
- Always include fallback behavior for non-JavaScript users
- Use valid HTML structure compatible with older browsers

### CSS Guidelines
- **Minimal and functional** - Only styles necessary for demonstration
- Use CSS custom properties for consistent theming
- Prefer CSS Grid/Flexbox over complex positioning
- Include basic responsive design (mobile-friendly)
- Highlight HTMX-specific states (loading, swapping, etc.)

**Base CSS Variables**:
```css
:root {
  --primary-color: #3b82f6;
  --success-color: #10b981;
  --error-color: #ef4444;
  --border-color: #d1d5db;
  --text-color: #374151;
  --bg-color: #ffffff;
}
```

### JavaScript Rules
- **Absolutely minimal** JavaScript outside of HTMX
- Only use JS for features that cannot be achieved with HTMX + server-side logic
- Document any JavaScript with comments explaining why HTMX alone wasn't sufficient
- Prefer CSS animations over JavaScript animations

## 📚 Documentation Standards

### Example README Template
Each example should include:
```markdown
# Example Name

## HTMX Features Demonstrated
- Primary: `hx-get`, `hx-target`
- Secondary: `hx-indicator`, `hx-trigger`

## User Story
As a user, I want to [action] so that [benefit].

## How It Works
1. User clicks button
2. HTMX sends GET request to `/api/data`
3. Server returns HTML fragment
4. HTMX replaces content in target div

## Try It Out
1. `cd example-name`
2. `pipenv install`
3. `pipenv run python myapp.py`
4. Visit http://localhost:5000

## Learning Points
- Demonstrates lazy loading pattern
- Shows how HTMX handles loading states
- Example of progressive enhancement
```

### Code Comments
- **HTMX attributes**: Explain purpose and behavior
- **Flask routes**: Document what HTML is returned and why
- **Key interactions**: Explain the user flow and server communication

## 🚀 Quality Checklist

Before considering an example complete, verify:

### Functionality
- [ ] Works without JavaScript (graceful degradation)
- [ ] Works with JavaScript disabled, then enabled
- [ ] Demonstrates the HTMX feature clearly
- [ ] Handles error states appropriately
- [ ] Mobile-friendly responsive design

### Code Quality
- [ ] Follows naming conventions
- [ ] Minimal external dependencies
- [ ] Self-documenting code structure
- [ ] Proper HTML semantics and accessibility
- [ ] Comments explain HTMX-specific behavior

### Documentation
- [ ] Clear example README
- [ ] Inline code comments for learning
- [ ] User story and learning objectives defined
- [ ] Setup instructions work from scratch

### Performance
- [ ] Minimal CSS (< 50 lines for basic examples)
- [ ] Minimal JavaScript (ideally 0 lines beyond HTMX)
- [ ] Fast server responses
- [ ] Efficient HTMX usage (right attributes for the job)

## 🎨 Design Philosophy

### Visual Design
- **Clean and minimal** - Focus on functionality over aesthetics
- **Consistent** - Similar spacing, colors, and typography across examples
- **Accessible** - Proper contrast, keyboard navigation, screen reader support
- **Responsive** - Works on mobile and desktop

### User Experience
- **Immediate feedback** - Loading indicators, success states, error handling
- **Intuitive interactions** - Standard web patterns, clear affordances
- **Forgiving** - Handle user errors gracefully
- **Fast** - Quick server responses, minimal loading times

## 🔧 Technical Constraints

### Browser Support
- Modern browsers (Chrome, Firefox, Safari, Edge)
- No Internet Explorer support required
- Mobile browser compatibility

### Performance Targets
- Page load time: < 1 second
- HTMX request time: < 500ms
- CSS file size: < 10KB per example
- HTML semantics score: 90%+

## 📖 Anti-Patterns to Avoid

### ❌ Don't Do This
- **Over-engineering**: Complex state management when simple server-side logic would work
- **Feature creep**: Adding unrelated functionality to demonstrate "real-world" usage
- **JavaScript fallbacks**: Using JS to replicate HTMX functionality
- **Heavy frameworks**: Including React/Vue/etc. "just for one small part"
- **Complex build processes**: Webpack, bundlers, or preprocessing when simple files work
- **Non-semantic HTML**: `<div>` buttons, missing form labels, etc.

### ✅ Do This Instead
- **Server-side thinking**: Handle state and logic on the server when possible
- **Progressive enhancement**: Start with working HTML, enhance with HTMX
- **Semantic HTML**: Use proper elements for their intended purpose
- **Simple file structure**: Direct file serving without build steps
- **Clear separation**: HTMX for interaction, CSS for presentation, minimal JS for edge cases

## 🎯 Success Metrics

An example is successful when:
- A developer new to HTMX can understand it in < 5 minutes
- The core HTMX feature is demonstrated clearly
- The code can be copied and adapted to other projects
- The interaction feels smooth and responsive
- The example inspires developers to explore HTMX further

---

**Remember**: We're building a reference library, not a production application. Prioritize **clarity**, **education**, and **simplicity** over **completeness** or **real-world complexity**. 