# HTMX Flask Examples

**Version: $NEW_VERSION**

A comprehensive collection of HTMX examples with Flask backend, designed to demonstrate modern web development patterns without JavaScript frameworks.

## 🚀 Quick Start

```bash
# Install dependencies for all examples
make install

# Run a specific example
cd ACTIVESEARCH && python myapp.py
# Then visit http://localhost:5000
```

## 📁 Project Structure

This project contains three educational HTMX examples:

### 1. **ACTIVESEARCH** - Live Search with Debouncing
- Real-time search with 500ms debounce
- Demonstrates `hx-post`, `hx-trigger`, `hx-target`, `hx-indicator`
- 24 sample users with Hispanic names
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
<script src="https://unpkg.com/htmx.org@2.0.6/dist/htmx.min.js"></script>
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




