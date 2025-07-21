# HTMX Flask Examples

**Version: 0.9.3**

![CI](https://github.com/yourusername/htmxflask/workflows/CI/badge.svg)

A comprehensive collection of HTMX examples with Flask backend, designed to demonstrate modern web development patterns without JavaScript frameworks.

## 🚀 Quick Start

```bash
# Install dependencies for all examples
make install

# Run a specific example
cd ACTIVESEARCH && uv run myapp.py
# Then visit http://localhost:5000
```

## 📁 Project Structure

This project contains six educational HTMX examples:

### 1. **ACTIVESEARCH** - Live Search with Debouncing
- Real-time search with 500ms debounce
- Demonstrates `hx-post`, `hx-trigger`, `hx-target`, `hx-indicator`
- 24 sample users more names
- Loading indicators and error handling

### 2. **VALUESELECT** - Cascading Dropdowns
- Dynamic model loading based on make selection
- Demonstrates `hx-get`, `hx-target`, `hx-trigger`
- Comprehensive car database with 400+ makes and models
- Server-side data filtering

### 3. **PLY3** - Mutually Exclusive Dropdowns
- Constraint-based form interactions
- Demonstrates `hx-post`, `hx-target`
- Server-side state management
- Template-based HTML generation

### 4. **PROGRESSBAR** - Real-time Progress Bar
- Self-polling progress bar with live updates every 600ms
- Demonstrates `hx-post`, `hx-trigger="every 600ms"`, `hx-target`, `HX-Trigger`
- Based on official HTMX progress bar example
- Simple state management with 5% increments and smooth CSS transitions
- Full accessibility support with ARIA attributes

### 5. **CLICKEDIT** - Inline Editing
- Click-to-edit contact information with inline form replacement
- Demonstrates `hx-get`, `hx-put`, `hx-target`, `hx-swap`
- Based on official HTMX click-to-edit example
- Form validation and cancel functionality
- Educational code with comprehensive HTMX comments

### 6. **CLICKLOAD** - Lazy Loading
- Progressive loading of contacts with pagination
- Demonstrates `hx-get`, `hx-target`, `hx-swap` for lazy loading
- Based on official HTMX click-to-load example
- Loading indicators and "Load More" functionality
- Efficient pagination with 3 contacts per page (24 total contacts across 8 pages)

## 🛠️ Development Tools

### Makefile Commands
```bash
make help                    # Show all available commands
make install                 # Install dependencies for all examples
make test                    # Run linting and tests
make clean                   # Clean up temporary files
make version VERSION=0.4.0   # Update version and create git tag
make pre-git-commit          # Clean invisible characters before commit
```

### HTMX Configuration
All examples use a minimal HTMX configuration for educational purposes:

```html
<script src="https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js"></script>
<script>
  // Minimal configuration for educational examples
  htmx.config.historyEnabled = false;
  htmx.config.allowEval = false;
  htmx.config.allowScriptTags = false;
</script>
```

## 📚 Documentation

- **[Changelog](docs/CHANGELOG.md)** - Version history and changes
- **[Development Guiding Light](docs/DEVGUIDINGLIGHT.md)** - Development standards
- **[Features Documentation](docs/FEATURES.md)** - Detailed feature descriptions

## 🔧 Development Workflow

This project follows strict development standards:

1. **Version Management**: All changes require version bumping
2. **Documentation**: Updates must be documented in changelog
3. **Code Quality**: Invisible character cleaning before commits
4. **Linting**: Automated code quality checks

## 🚀 CI/CD Pipeline

This project uses GitHub Actions for continuous integration and testing:

### Automated Testing
- **Trigger**: Runs on every push to main/master and pull requests
- **Environment**: Ubuntu with Python 3.11 and uv package manager
- **Tests**: All 6 HTMX examples with comprehensive test suites
- **Linting**: Automated code quality checks with flake8

### Workflow Files
- **`.github/workflows/ci.yml`**: Main CI pipeline with test summary
- **`.github/workflows/test.yml`**: Multi-Python version testing (3.9, 3.10, 3.11)

### Test Coverage
The CI pipeline validates:
- ✅ **ACTIVESEARCH**: Search functionality with HTMX patterns
- ✅ **VALUESELECT**: Cascading dropdowns with data loading
- ✅ **PLY3**: Interdependent dropdowns with mutual exclusion
- ✅ **PROGRESSBAR**: Real-time progress with polling
- ✅ **CLICKEDIT**: Inline editing with form handling
- ✅ **CLICKLOAD**: Lazy loading with pagination

### HTMX Patterns Validated
- `hx-get`, `hx-post`, `hx-put` - HTTP methods
- `hx-target`, `hx-swap` - DOM manipulation
- `hx-trigger`, `hx-indicator` - Event handling and loading states
- Real-time updates and form validation

### Status Badge
Add this badge to your README to show CI status:
```markdown
![CI](https://github.com/yourusername/htmxflask/workflows/CI/badge.svg)
```

See [`.cursorrules`](.cursorrules) for complete development guidelines.

## 🏗️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTMX 2.0.6 (CDN)
- **Package Management**: uv
- **Development**: Makefile automation
- **Code Quality**: flake8 linting

## 🎯 Learning Objectives

Each example demonstrates specific HTMX patterns:
- **Server-side rendering** without JavaScript frameworks
- **Progressive enhancement** with minimal client-side code
- **Real-time interactions** using HTMX attributes
- **Error handling** and user feedback
- **Responsive design** with CSS

## 📖 Original Examples

For the original HTMX examples, visit: https://htmx.org/examples/

This project reimplements those examples with Flask backends to show the complete server-side implementation required.




