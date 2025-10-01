# HTMX Flask Examples

**Version: 0.20.0**

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

This project contains fourteen educational HTMX examples:

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

### 7. **LAZYLOAD** - Automatic Content Loading
- Content loads automatically when page loads
- Demonstrates `hx-get`, `hx-trigger="load"`, `hx-indicator`, `.htmx-settling`
- Based on official HTMX lazy-load example
- Smooth fade-in animations using CSS transitions
- Revenue analytics dashboard with 12 months of data

### 8. **INLINVALIDATION** - Real-time Form Validation
- Real-time form field validation with server feedback
- Demonstrates `hx-post`, `hx-trigger="input changed delay:300ms"`, `hx-target`, `hx-indicator`
- Based on official HTMX inline-validation example
- Debounced validation to prevent excessive requests
- Comprehensive validation for username, email, password, and age

### 9. **FILEUPLOAD** - Drag-and-Drop File Upload
- Modern file upload with drag-and-drop interface
- Demonstrates `hx-post`, `hx-encoding="multipart/form-data"`, `hx-indicator`, progress tracking
- Based on official HTMX file-upload example
- Real-time progress indicators and multiple file support
- Comprehensive security validation and error handling

### 10. **DELETEROW** - Row Deletion with Animation
- Delete table rows with confirmation and fade-out animation
- Demonstrates `hx-delete`, `hx-confirm`, `hx-target="closest tr"`, `hx-swap="outerHTML swap:1s"`
- Based on official HTMX delete-row example
- Smooth 1-second fade-out animation before row removal
- RESTful DELETE endpoints with proper HTTP methods

### 11. **EDITROW** - Editable Table Rows
- Edit table rows inline with single-instance editing
- Demonstrates `hx-get`, `hx-put`, `hx-target="closest tr"`, `hx-swap="outerHTML"`
- Custom event triggers (`hx-trigger="edit"`) with JavaScript integration
- Form data handling with `hx-include="closest tr"`
- Cancel functionality with `hx-trigger="cancel"`
- Based on official HTMX edit-row example
- Visual feedback with highlighted editing rows

### 12. **BULKUPDATE** - Bulk Operations with Checkboxes

### 13. **FILEUPLOADPRESERVE** - File Upload Input Preservation
- Preserve file selections after form validation errors
- Demonstrates `hx-preserve`, `hx-post`, `hx-target`, `hx-swap="outerHTML"`
- Based on official HTMX file-upload-input example
- Side-by-side comparison showing with/without `hx-preserve`
- Server-side validation with file input preservation

### 14. **RESETINPUT** - Reset User Input
- Automatically reset form inputs after successful requests
- Demonstrates `hx-on::after-request`, `hx-post`, `hx-target`, `hx-swap="afterbegin"`
- Based on official HTMX reset-user-input example
- Dual method demonstration (form reset vs individual input reset)
- Event listener approach to avoid `htmx:evalDisallowedError`

## 🛠️ Development Tools

### Makefile Commands
```bash
make help                    # Show all available commands
make install                 # Install dependencies for all examples
make test                    # Run linting and tests
make clean                   # Clean up temporary files
make version VERSION=0.4.0   # Update version and create git tag
make pre-git-commit          # Clean invisible characters before commit
make test-example EXAMPLE=DELETEROW  # Test specific example
make test-example EXAMPLE=BULKUPDATE  # Test specific example
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
- **[Features Documentation](.docs/FEATURES.md)** - Detailed feature descriptions and roadmap
- **[GitHub Actions Guide](docs/GITHUB_ACTIONS.md)** - CI/CD pipeline documentation

## 🔧 Development Workflow

This project follows strict development standards:

1. **Version Management**: All changes require version bumping
2. **Documentation**: Updates must be documented in changelog
3. **Code Quality**: Invisible character cleaning before commits
4. **Linting**: Automated code quality checks
5. **Pre-commit Hooks**: Automatic validation before commits

### Version Management & Git Tagging

This project uses automated version management with git tagging for releases:

#### Version Bumping
```bash
# Bump version (patch, minor, major, or feature)
make version-update TYPE=feature    # 0.19.0 → 0.20.0
make version-update TYPE=minor      # 0.19.0 → 0.20.0
make version-update TYPE=major      # 0.19.0 → 1.0.0
make version-update TYPE=patch      # 0.19.0 → 0.19.1
```

#### Git Tag Creation
```bash
# Create annotated tag for current version
git tag -a v0.20.0 -m "Release v0.20.0: Feature description"

# Push tag to GitHub
git push origin v0.20.0
```

#### Complete Release Workflow
1. **Make changes** and test thoroughly
2. **Bump version**: `make version-update TYPE=feature`
3. **Update documentation**: README.md, CHANGELOG.md, FEATURES.md
4. **Clean whitespace**: `python scripts/clean_invisible_chars.py . --clean`
5. **Run tests**: `make test`
6. **Commit changes**: `git add . && git commit -m "feat: Description"`
7. **Create tag**: `git tag -a v0.20.0 -m "Release v0.20.0: Description"`
8. **Push everything**: `git push origin main && git push origin v0.20.0`

#### Version Types
- **feature**: New functionality (minor version bump)
- **minor**: New features, backward compatible
- **major**: Breaking changes
- **patch**: Bug fixes, backward compatible

#### Tag Message Format
```bash
git tag -a v0.20.0 -m "Release v0.20.0: Add RESETINPUT example with security-compliant JavaScript

Features:
- RESETINPUT example demonstrating automatic form input reset
- Event listener approach to avoid htmx:evalDisallowedError
- 24 comprehensive unit tests
- Minimal CSS following Development Guiding Light principles
- Educational documentation with troubleshooting guide
- Security-compliant JavaScript implementation

Examples: 14/47 completed (29.8%)
HTMX Patterns: hx-on::after-request, hx-post, hx-target, hx-swap"
```

#### GitHub Integration
- **Tags URL**: https://github.com/cscortes/htmxflask/releases/tag/v0.20.0
- **Releases Page**: https://github.com/cscortes/htmxflask/releases
- **Version History**: `git tag -l --sort=-version:refname`


## 🚀 CI/CD Pipeline
- **Release Checklist**: [docs/RELEASECHECKLIST.md](docs/RELEASECHECKLIST.md) - Complete release procedures


This project uses GitHub Actions for continuous integration and testing:

### Automated Testing
- **Trigger**: Runs on every push to main/master and pull requests
- **Environment**: Ubuntu with Python 3.9 and uv package manager
- **Tests**: All 13 HTMX examples with comprehensive test suites
- **Linting**: Automated code quality checks with flake8

### Workflow Files
- **`.github/workflows/ci.yml`**: Main CI pipeline with test summary
- **`.github/workflows/test.yml`**: Python 3.9 testing

### Test Coverage
The CI pipeline validates:
- ✅ **ACTIVESEARCH**: Search functionality with HTMX patterns
- ✅ **VALUESELECT**: Cascading dropdowns with data loading
- ✅ **PLY3**: Interdependent dropdowns with mutual exclusion
- ✅ **PROGRESSBAR**: Real-time progress with polling
- ✅ **CLICKEDIT**: Inline editing with form handling
- ✅ **CLICKLOAD**: Lazy loading with pagination
- ✅ **DELETEROW**: Row deletion with animation and confirmation
- ✅ **EDITROW**: Editable table rows with single-instance editing
- ✅ **BULKUPDATE**: Bulk operations with checkboxes and form handling

### HTMX Patterns Validated
- `hx-get`, `hx-post`, `hx-put` - HTTP methods
- `hx-target`, `hx-swap` - DOM manipulation
- `hx-trigger`, `hx-indicator` - Event handling and loading states
- `hx-delete`, `hx-confirm` - Row deletion and confirmation
- `hx-swap="innerHTML settle:3s"` - Bulk operations with settling animations
- Real-time updates and form validation

### Status Badge
Add this badge to your README to show CI status:
```markdown
![CI](https://github.com/yourusername/htmxflask/workflows/CI/badge.svg)
```

See [`.cursorrules`](.cursorrules) for complete development guidelines.

## 🏗️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTMX 2.0.3 (CDN)
- **Package Management**: uv
- **Development**: Makefile automation
- **Code Quality**: flake8 linting
- **Testing**: unittest framework with comprehensive test suites
- **CI/CD**: GitHub Actions with automated testing and deployment

## 🎯 Learning Objectives

Each example demonstrates specific HTMX patterns:
- **Server-side rendering** without JavaScript frameworks
- **Progressive enhancement** with minimal client-side code
- **Real-time interactions** using HTMX attributes
- **Error handling** and user feedback
- **Responsive design** with CSS
- **RESTful operations** with proper HTTP methods (GET, POST, PUT, DELETE)
- **User confirmation** and smooth animations

## 📖 Original Examples

For the original HTMX examples, visit: https://htmx.org/examples/

This project reimplements those examples with Flask backends to show the complete server-side implementation required.
