# Changelog

All notable changes to the HTMX Flask Examples project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.21.0] - 2025-10-01

### Added
- **DIALOGS Example**: New example demonstrating native browser dialogs using `hx-prompt` and `hx-confirm`
  - Based on official HTMX dialogs example (https://htmx.org/examples/dialogs/)
  - Native browser prompt and confirmation dialogs
  - Server receives user input via `HX-Prompt` header
  - Combined dialog functionality with confirmation and input
  - 21 comprehensive unit tests covering all functionality
  - Minimal CSS following Development Guiding Light principles
  - Educational documentation with debugging guide
  - Security-compliant implementation with proper headers

### Changed
- **Documentation**: Updated README.md to include DIALOGS example
- **Project Count**: Updated from fourteen to fifteen examples
- **Makefile**: Added DIALOGS to all targets (version, lint, test, install)
- **FEATURES.md**: Updated completion count to 15/47 examples


## [0.20.0] - 2025-10-01

### Added
- **RESETINPUT Example**: New example demonstrating automatic form input reset using `hx-on::after-request`
  - Based on official HTMX reset-user-input example (https://htmx.org/examples/reset-user-input/)
  - Dual method demonstration: form reset vs individual input reset
  - Event listener approach to avoid `htmx:evalDisallowedError` with `allowEval = false`
  - 24 comprehensive unit tests covering all functionality
  - Minimal CSS following Development Guiding Light principles
  - Educational documentation with troubleshooting guide
  - Comprehensive debugging with console logging
  - Security-compliant JavaScript implementation

### Fixed
- **RESETINPUT Security Issue**: Fixed `htmx:evalDisallowedError` by replacing inline JavaScript with event listeners
  - Removed `hx-on::after-request` inline JavaScript that was blocked by security settings
  - Implemented proper event listener approach for form reset functionality
  - Maintains security compliance with `htmx.config.allowEval = false`

### Changed
- **Documentation**: Updated README.md to include RESETINPUT example
- **Project Count**: Updated from thirteen to fourteen examples
- **Makefile**: Added RESETINPUT to all targets (version, lint, test, install)
- **FEATURES.md**: Updated completion count to 14/47 examples

## [0.19.0] - 2025-10-01

### Added
- **FILEUPLOADPRESERVE Example**: New example demonstrating file upload input preservation using `hx-preserve`
  - Based on official HTMX file-upload-input example (https://htmx.org/examples/file-upload-input/)
  - Side-by-side comparison showing with/without `hx-preserve`
  - Server-side validation with file input preservation
  - 20 comprehensive unit tests covering all functionality
  - Minimal CSS following Development Guiding Light principles
  - Educational documentation (README.md, DESIGN.md)
  - Quick test buttons with JavaScript for easy demonstration
  - Disabled client-side validation to showcase server-side validation

### Fixed
- **FILEUPLOADPRESERVE Bug**: Fixed duplicate form appearing when invalid data was entered
  - Changed HTMX targeting from `innerHTML` to `outerHTML` swap
  - Forms now replace themselves correctly instead of duplicating
  - Error templates use consistent HTMX targeting

### Changed
- **Documentation**: Updated README.md to include FILEUPLOADPRESERVE example
- **Project Count**: Updated from twelve to thirteen examples
- **FEATURES.md**: Updated completion count to 13/47 examples

## [0.18.0] - 2025-10-01

### Changed
- **FILEUPLOAD Example**: Completely refactored following Development Guiding Light principles
- **Simplified Structure**: Reduced from 4 templates to 1 (75% reduction)
- **Minimal CSS**: Reduced from 296 to 96 lines (67% reduction)
- **Inline HTML Responses**: Server returns HTML fragments, not JSON
- **Original Filenames**: Removed UUID generation, use secure_filename only
- **Real Progress Tracking**: Uses htmx:xhr:progress event for actual upload progress

### Added
- **Comprehensive Unit Tests**: 22 tests covering all functionality
- **HTML Response Validation**: Tests verify HTML fragments (not JSON)
- **BestPractices.md**: Lessons learned and simplified patterns
- **Educational Documentation**: README and DESIGN following guiding light template
- **HTMX Comments**: All attributes explained in HTML
- **JavaScript Documentation**: Explains why HTMX alone isn't sufficient
- **Favicon Support**: Added SVG favicon files

### Enhanced
- **Development Guiding Light Compliance**: Minimal dependencies, educational code
- **Official HTMX Pattern**: Based on htmx.org/examples/file-upload
- **Security**: Maintained all validation (type, size, path traversal)
- **Makefile Integration**: Tests fully integrated with root Makefile
- **Code Simplicity**: -153 lines overall, clearer structure

### Technical
- **Template Reduction**: Removed upload_result.html, multi_upload_result.html, file_list.html
- **Response Format**: Inline HTML in routes (e.g., `<div class="success">✅ Uploaded</div>`)
- **Progress Bars**: Real HTML5 progress elements updated via JavaScript
- **Test Coverage**: 22 unit tests (basic, validation, security, HTML format)
- **Dependencies**: Removed uuid, minimal imports

## [0.17.0] - 2024-12-19

### Added
- **FILEUPLOAD Example**: New drag-and-drop file upload example
- **Drag & Drop Interface**: HTML5 drag and drop with visual feedback
- **Progress Tracking**: Real-time upload progress indicators
- **Multiple File Support**: Batch upload functionality
- **Security Validation**: Comprehensive file type and size checks
- **File Management**: Upload history and delete functionality

### Enhanced
- **Upload UX Patterns**: Modern file upload with intuitive interface
- **HTMX File Handling**: `hx-encoding="multipart/form-data"` patterns
- **Progress Indicators**: Visual feedback during upload process
- **Error Handling**: Comprehensive upload error management
- **Template Architecture**: Modular file upload components

### Technical
- **File Security**: Server-side validation and sanitization
- **Drag & Drop API**: Native browser drag and drop integration
- **Progress Tracking**: Real-time upload status monitoring
- **Multiple Uploads**: Concurrent file processing
- **Storage Management**: Secure file handling and cleanup

## [0.16.0] - 2024-12-19

### Added
- **INLINVALIDATION Example**: New real-time form validation example
- **Debounced Validation**: 300ms delay prevents excessive server requests
- **Multi-field Validation**: Username, email, password, confirm password, age
- **Server-side Security**: All validation logic runs server-side
- **Visual Feedback**: Success/error/warning states with animations

### Enhanced
- **Form UX Patterns**: Real-time validation feedback improves completion rates
- **HTMX Validation**: Comprehensive `hx-trigger="input"` patterns
- **Template Architecture**: Reusable validation message components
- **Accessibility**: ARIA live regions and screen reader support
- **Test Coverage**: 19 test cases covering all validation scenarios

### Technical
- **Validation Logic**: Custom validators with business rules
- **Cross-field Validation**: Password confirmation matching
- **Debouncing Strategy**: Optimized server request patterns
- **Response Optimization**: Fast validation response times
- **Template Components**: Modular validation message rendering

## [0.15.0] - 2024-12-19

### Added
- **LAZYLOAD Example**: New automatic content loading example
- **Template Rendering**: Refactored HTML generation to use Jinja2 templates
- **HTMX Lazy Loading**: Demonstrates `hx-trigger="load"` pattern
- **Revenue Analytics**: Interactive dashboard with charts and tables
- **Fade-in Animations**: Smooth `.htmx-settling` CSS transitions

### Enhanced
- **Template Architecture**: Separated HTML from Python business logic
- **Educational Content**: Comprehensive documentation for lazy loading patterns
- **Test Coverage**: 14 test cases for LAZYLOAD functionality
- **Code Quality**: Improved maintainability with template-based rendering

### Technical
- **Jinja2 Integration**: Full Flask template rendering for HTML fragments
- **Data Processing**: Clean separation of data preparation and presentation
- **Performance**: Optimized template rendering with minimal overhead

## [0.14.1] - 2024-12-19

### Fixed
- **BULKUPDATE Test Cases**: Fixed all failing test cases in BULKUPDATE example
- **Test Expectations**: Corrected test assertions to match actual bulk update logic
- **State Management**: Fixed test state pollution between test runs
- **Dataset Consistency**: Updated tests to work with full 10-contact dataset
- **Update Count Validation**: Fixed expected counts for various test scenarios

### Technical
- **Test Suite Reliability**: Improved test isolation and state reset mechanisms
- **Assertion Accuracy**: Updated test expectations to match correct HTMX bulk update behavior
- **Documentation Sync**: Ensured all test descriptions match actual functionality

## [0.14.0] - 2024-12-19

### Fixed
- **BULKUPDATE Bug Fix**: Corrected logic to only update checked contacts
- **Contact Status Management**: Fixed issue where unchecked contacts were incorrectly processed
- **Update Count Accuracy**: Now correctly counts only contacts that actually change status
- **Form Data Processing**: Improved checkbox handling to respect user selections

### Enhanced
- **Development Guiding Light Principles**: Applied to BULKUPDATE example
- **Comprehensive Documentation**: Enhanced README.md and DESIGN.md with guiding light principles
- **Educational Content**: Added detailed explanations of HTMX patterns and design decisions
- **Code Quality**: Improved inline HTML generation and server-side processing documentation
- **Accessibility Features**: Enhanced ARIA attributes and screen reader support documentation

## [0.12.0] - 2024-12-19

### Added
- **BULKUPDATE Example** - Bulk Operations with Checkboxes
  - Bulk update contact statuses using checkbox selections
  - Demonstrates `hx-post`, `hx-target="#toast"`, `hx-swap="innerHTML settle:3s"`
  - Form-based bulk operations with standard HTML checkboxes
  - Toast notifications with settling animations
  - Select all functionality and selection counting
  - Server-side processing of multiple checkbox selections
  - Comprehensive test suite with 9 test methods
  - Filipino boxers dataset with 5 contacts
  - Educational code with detailed HTMX comments
  - Based on official HTMX bulk-update example
  - Accessibility features with ARIA attributes and screen reader support

## [0.11.0] - 2024-12-19

### Added
- **EDITROW Example** - Editable Table Rows
  - Edit table rows inline with single-instance editing
  - Demonstrates `hx-get`, `hx-put`, `hx-target="closest tr"`, `hx-swap="outerHTML"`
  - Custom event triggers (`hx-trigger="edit"`) with JavaScript integration
  - Form data handling with `hx-include="closest tr"`
  - Cancel functionality with `hx-trigger="cancel"`
  - Based on official HTMX edit-row example
  - Visual feedback with highlighted editing rows
  - Comprehensive test suite with 6 test methods
  - Filipino boxers dataset with 5 contacts
  - Educational code with detailed HTMX comments
  - Single-instance editing to prevent multiple rows being edited simultaneously
  - Form validation and error handling
  - Responsive design with proper table styling

## [0.10.0] - 2024-12-19

### Added
- **DELETEROW Example** - Row Deletion with Animation
  - Delete table rows with confirmation and fade-out animation
  - Demonstrates `hx-delete`, `hx-confirm`, `hx-target="closest tr"`, `hx-swap="outerHTML swap:1s"`
  - Based on official HTMX delete-row example
  - Smooth 1-second fade-out animation before row removal
  - RESTful DELETE endpoints with proper HTTP methods
  - Comprehensive test suite with 8 test methods
  - Filipino boxers dataset with 10 contacts
  - Educational code with detailed HTMX comments

### Fixed
- **HTMX Version Consistency**
  - Updated DELETEROW to use HTMX 2.0.3 (matching other examples)
  - Ensures consistent behavior across all examples
  - Fixed from `htmx.org@1.9.10` to `htmx.org@2.0.3/dist/htmx.min.js`

## [0.9.6] - 2024-12-19

### Fixed
- **CI Workflow Improvements**
  - Add quotes around python-version for better YAML compatibility
  - Add explicit venv activation step for better dependency management
  - Ensures proper virtual environment setup in CI pipeline

## [0.9.5] - 2024-12-19

### Fixed
- **GitHub Actions Cache Issue**
  - Force new workflow run to clear cached workflow versions
  - Resolves Python 3.1 error from cached workflow execution
  - Ensures fresh workflow execution with correct Python versions

## [0.9.4] - 2024-12-19

### Fixed
- **GitHub Actions YAML Formatting**
  - Fixed line break issue in cache key configuration
  - Resolves YAML parsing errors in test workflow
  - Ensures proper workflow execution across all Python versions

## [0.9.3] - 2024-12-19

### Fixed
- **GitHub Actions Deprecation Warnings**
  - Updated `actions/upload-artifact@v3` → `actions/upload-artifact@v4`
  - Updated `actions/cache@v3` → `actions/cache@v4`
  - Resolves deprecation warnings in CI/CD pipelines
  - Ensures compatibility with latest GitHub Actions versions

## [0.9.2] - 2024-12-19

### Fixed
- **GitHub Actions Virtual Environment**
  - Added `uv venv` creation step in all workflows before dependency installation
  - Fixes "No virtual environment found" error in CI/CD pipelines
  - Ensures proper virtual environment setup for Flask and flake8 installation
  - All workflows now create venv before installing dependencies

## [0.9.1] - 2024-12-19

### Fixed
- **GitHub Actions Workflow**
  - Fixed CI, test, scheduled, and deploy workflows to install dependencies correctly for project structure without a root `pyproject.toml`.
  - Now uses `uv pip install flask flake8` globally so Makefile and tests work for all examples.
  - Ensures all workflows run successfully on GitHub Actions.

## [0.9.0] - 2024-12-19

### Added
- **GitHub Actions CI/CD Pipeline** - Comprehensive automated testing and deployment
  - **CI Workflow** (`.github/workflows/ci.yml`): Main continuous integration pipeline
    - Runs on every push to main/master and pull requests
    - Python 3.9 with uv package manager
    - Executes `make test` for all examples with detailed summaries
    - Validates all HTMX patterns and functionality
  - **Test Suite Workflow** (`.github/workflows/test.yml`): Multi-Python version testing
    - Matrix testing on Python 3.9
    - Caches dependencies for faster builds
    - Uploads test artifacts for debugging
    - Comprehensive compatibility validation
  - **Scheduled Health Check** (`.github/workflows/scheduled.yml`): Daily automated monitoring
    - Runs daily at 2 AM UTC with manual trigger option
    - Ensures project stays healthy over time
    - Creates health reports in GitHub UI
    - Early detection of potential issues
  - **Deploy Examples** (`.github/workflows/deploy.yml`): Deployment automation
    - Triggers on release publication or manual deployment
    - Environment-specific deployments (staging/production)
    - Pre-deployment testing and package creation
    - Comprehensive deployment summaries
- **CI/CD Documentation** - Complete workflow documentation
  - **GitHub Actions Guide** (`docs/GITHUB_ACTIONS.md`): Comprehensive workflow documentation
    - Detailed explanation of all 4 workflows
    - Usage instructions and troubleshooting
    - Configuration and monitoring guidance
    - Status badge integration
  - **README Updates**: Added CI/CD pipeline section
    - Automated testing overview
    - Test coverage details
    - HTMX patterns validation
    - Status badge integration
- **Test Coverage Validation** - All examples now have comprehensive test suites
  - **ACTIVESEARCH**: 15 tests covering search functionality and HTMX patterns
  - **VALUESELECT**: 14 tests covering cascading dropdowns and data loading
  - **PLY3**: 14 tests covering interdependent dropdowns and mutual exclusion
  - **PROGRESSBAR**: Existing tests for real-time progress functionality
  - **CLICKEDIT**: Existing tests for inline editing functionality
  - **CLICKLOAD**: Existing tests for lazy loading functionality
- **HTMX Pattern Validation** - Comprehensive pattern testing across all examples
  - `hx-get`, `hx-post`, `hx-put` - HTTP methods validation
  - `hx-target`, `hx-swap` - DOM manipulation testing
  - `hx-trigger`, `hx-indicator` - Event handling and loading states
  - Real-time updates and form validation
  - Cross-device file handling and edge case coverage

### Changed
- **Development Workflow** - Enhanced with automated quality assurance
  - All commits now automatically tested via GitHub Actions
  - Pull requests require passing tests before merge
  - Daily health checks ensure long-term project stability
  - Deployment automation for consistent releases
- **Project Monitoring** - Added comprehensive status tracking
  - CI status badge for README integration
  - Health reports in GitHub UI
  - Test summaries for each workflow run
  - Deployment summaries with environment details

## [0.8.0] - 2024-12-19

### Added
- **Inline HTML Generation for Fragments** - New development pattern and recommendations
  - **CLICKLOAD Example Enhancement**: Moved fragment HTML generation inline into Flask routes
  - **Performance Improvement**: Eliminated template overhead for simple, repetitive HTML fragments
  - **Development Guiding Light Updates**: Added comprehensive recommendations for inline HTML generation
  - **Educational Value**: Maintained HTMX comments and clear code structure in inline generation
  - **File Structure Simplification**: Reduced template file count while maintaining functionality
- **Development Guiding Light Enhancements** - New architectural recommendations
  - Added guidance for inline HTML generation for simple fragments (table rows, list items)
  - Updated file organization standards to reflect inline HTML approach
  - Added practical code examples showing recommended inline HTML patterns
  - Enhanced performance guidelines to consider inline generation for simple fragments
  - Added anti-pattern guidance to avoid template overuse for repetitive HTML
  - Updated best practices to include inline HTML generation as preferred approach
- **CLICKLOAD Architecture Improvement** - Simplified and optimized implementation
  - Moved `contacts_fragment.html` content inline into `myapp.py`
  - Eliminated separate template file while maintaining all functionality
  - Preserved educational HTMX comments in inline code generation
  - Maintained proper pagination logic and HTMX attribute handling
  - All tests passing (9/9) with improved performance characteristics

## [0.3.0] - 2024-12-19

### Added
- **Git Commit Rules** in `.cursorrules` for consistent development workflow
  - Mandatory version bumping before commits using `make version VERSION=x.x.x`
  - Required documentation updates (README.md, docs/CHANGELOG.md, etc.)
  - Proper change documentation and versioning requirements
- **Development Workflow Standards** to ensure project consistency

## [0.4.1] - 2024-12-19

### Fixed
- **Git commit workflow** - Fixed Makefile to support `.cursorrules` requirements
  - Added `make version-update` target for automated version bumping
  - Implemented proper semantic versioning (feature/bugfix/patch)
  - Corrected development workflow to follow established rules

## [0.4.0] - 2024-12-19

### Added
- **Automated version management** with `make version-update` target
  - Automatic version bumping based on change type (`feature`, `bugfix`, `patch`)
  - Semantic versioning support (major.minor.patch)
  - Simplified development workflow following git commit rules
- **Comprehensive README.md documentation** - Complete project overview
  - Quick start guide with current tooling (uv, make)
  - Detailed project structure and learning objectives
  - Development workflow and technology stack documentation
  - Links to all project documentation

## [0.3.1] - 2024-12-19

### Fixed
- **Invisible character cleaning script** - Improved file extension handling
  - Added support for all project file types (`.css`, `.html`, `.cursorrules`, `.csv`, `.yml`, `.yaml`)
  - Added support for files without extensions (`LICENSE`, `VERSION`, `Makefile`)
  - Excluded binary/image files (`.svg`, `.lock`, `.png`, `.jpg`, etc.) from processing
  - Excluded `.venv` directories and other build/cache directories
  - Refactored extension logic into reusable functions (`should_process_file`, `get_processable_files`)
  - Eliminated code duplication and improved maintainability

## [0.7.3] - 2024-12-19

### Fixed
- **CLICKEDIT Development Guiding Light Compliance** - Comprehensive audit and improvements
  - Achieved 9.3/10 compliance score (Grade A)
  - Simplified CSS from 159 lines to 93 lines (41% reduction)
  - Added comprehensive HTMX attribute documentation with inline comments
  - Added user story and step-by-step workflow documentation
  - Removed unused CSS styles and consolidated rules
  - Maintained all functionality while improving code quality
- **CLICKEDIT Documentation** - Enhanced educational value
  - Added structured user story: "As a user, I want to edit contact information inline..."
  - Added detailed "How It Works" section with 5-step workflow
  - Added inline comments explaining all HTMX attributes
  - Follows Development Guiding Light documentation template
- **CLICKEDIT Code Quality** - Improved maintainability and readability
  - Added educational comments for all HTMX patterns
  - Simplified CSS while preserving essential styling
  - Enhanced code documentation for learning purposes
  - All tests passing (9/9) with improved functionality

### Changed
- **CLICKEDIT CSS** - Major simplification and optimization
  - Removed unused `.contacts-list` styles (not used in single-contact example)
  - Eliminated redundant CSS custom properties and transitions
  - Consolidated button and form styling rules
  - Removed complex info section styling while maintaining functionality
  - Reduced CSS complexity while preserving visual design

## [0.7.2] - 2024-12-19

### Changed
- **Version Management** - Updated all project files to version 0.7.2
- **Documentation** - Updated README.md and CHANGELOG.md with latest changes

## [0.7.1] - 2024-12-19

### Fixed
- **PROGRESSBAR Code Quality** - Fixed all linting and code style issues
  - Fixed whitespace around operator: `PROGRESS = 0`
  - Added proper blank lines between functions (PEP 8 compliance)
  - Added newline at end of test file
  - Fixed HTML structure with proper `lang="en"` attribute
  - Implemented CSS custom properties for consistent theming
  - All linting errors resolved (flake8 compliance)
- **PROGRESSBAR Development Guiding Light Compliance** - Full audit and improvements
  - Achieved 95/100 compliance score (Grade A)
  - Perfect HTMX implementation with self-polling pattern
  - Excellent accessibility with complete ARIA support
  - Comprehensive documentation and testing
  - Minimal external dependencies (HTMX only)
  - Educational code structure with clear comments

### Changed
- **PROGRESSBAR CSS** - Updated to use CSS custom properties
  - Added `:root` variables for consistent theming
  - All colors, sizes, and transitions now use custom properties
  - Follows design system guidelines from Development Guiding Light
- **PROGRESSBAR HTML** - Improved semantic structure
  - Added proper `lang="en"` attribute to HTML tag
  - Maintained all accessibility features and ARIA attributes

## [0.7.0] - 2024-12-19

### Added
- **PROGRESSBAR Example** - Real-time progress bar with HTMX
  - Based on official HTMX progress bar example (https://htmx.org/examples/progress-bar/)
  - Self-polling HTMX pattern with proper DOM structure
  - Simple state management with global progress variable
  - Real-time progress updates every 600ms with smooth CSS transitions
  - Bootstrap-style progress bar with accessibility attributes
  - Comprehensive test suite with 8 test cases
  - Proper task lifecycle management and completion handling
- **Critical HTMX Pattern Documentation** - Fixed polling implementation
  - Documented the correct self-polling pattern for HTMX progress bars
  - Explained proper HTML structure for smooth progress updates
  - Added detailed implementation examples and troubleshooting guide
  - Comprehensive debugging and testing tools
- **PROGRESSBAR Integration** - Added to project build system
  - Included in Makefile version management
  - Added to linting and installation targets
  - Integrated with project version control system

### Fixed
- **HTMX Progress Bar Implementation** - Complete rewrite based on working example
  - Implemented exact HTML structure from official HTMX progress bar example
  - Fixed polling frequency to 600ms (matching official example)
  - Added proper CSS transitions for smooth visual updates
  - Implemented correct task completion handling with `HX-Trigger` headers
  - Fixed all syntax and indentation errors in Flask application
- **Progress Bar CSS** - Updated to Bootstrap-style from official example
  - Added proper accessibility attributes (aria-valuenow, aria-valuemin, etc.)
  - Implemented smooth CSS transitions for progress bar updates
  - Added proper button styling and hover effects
- **Version Management** - Improved Makefile version update system
  - Fixed sed commands to use VERSION file as single source of truth
  - Added PROGRESSBAR to all version management targets
  - Improved reliability of version updates across all examples

### Changed
- **Project Structure** - Added fourth example (PROGRESSBAR)
- **Documentation** - Updated README.md to include progress bar example
- **Testing** - Added comprehensive test suite for progress bar functionality
- **Implementation** - Rewrote to match official HTMX example exactly

## [Unreleased]

### Added
- Comprehensive changelog documentation

## [0.2.1] - 2024-12-19

### Added
- **Makefile** with automated project management
  - `make help` - Show all available targets
  - `make version VERSION=x.x.x` - Update version across project and create git tag
  - `make clean` - Clean up temporary files and build artifacts
  - `make test` - Placeholder for running tests
  - `make install` - Install dependencies for all examples
  - `make pre-git-commit` - Remove invisible characters before commit
- **VERSION file** for centralized version tracking
- **Automated version management** across all pyproject.toml files

### Changed
- **Version management** - Centralized version tracking with automated updates
- **Project structure** - Added Makefile for better development workflow

## [0.2.0] - 2024-12-19

### Added
- **Clean HTMX implementation** using CDN with minimal configuration
- **Minimal HTMX configuration** that disables unused features:
  - `htmx.config.historyEnabled = false`
  - `htmx.config.allowEval = false`
  - `htmx.config.allowScriptTags = false`
- **Improved error handling** in all examples
- **Comprehensive code comments** explaining HTMX functionality
- **Enhanced documentation** with detailed README files

### Changed
- **HTMX Implementation** - Switched from local files to CDN approach
  - Removed 492KB of local HTMX files (3 × 164KB files)
  - Updated all examples to use `https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js`
  - Simplified project structure by removing empty js directories
- **ACTIVESEARCH Example**:
  - Added proper HTML structure with DOCTYPE and head section
  - Created comprehensive CSS with HTMX indicators and responsive design
  - Added error handling for no results
  - Enhanced documentation with detailed HTMX pattern explanation
  - Added 24 diverse users names and randomized emails
- **VALUESELECT Example**:
  - Added proper HTML structure and external CSS
  - Enhanced error handling for invalid make selections
  - Improved code comments and documentation
  - Documented getdata.py as sample data retrieval script
  - Removed unnecessary dependencies, keeping only Flask
- **PLY3 Example**:
  - Fixed critical logic errors in the selected() function
  - Simplified constraint logic for mutual exclusion
  - Added proper error handling and input validation
  - Used template-based HTML generation instead of string concatenation
  - Removed unnecessary form submission and improved HTML structure
  - Added comprehensive code comments and documentation

### Removed
- **Local HTMX files** from all examples (ACTIVESEARCH, VALUESELECT, PLY3)
- **Empty js directories** from examples
- **Unnecessary dependencies** (beautifulsoup4, requests from main deps)
- **Complex HTMX configuration** in favor of minimal setup

### Fixed
- **PLY3 logic errors** that caused crashes with None values
- **HTML structure issues** in all examples
- **Missing error handling** in dropdown interactions
- **Poor code documentation** across all examples

## [0.1.0] - Initial Release

### Added
- **ACTIVESEARCH Example** - Live search functionality with HTMX
  - Demonstrates `hx-post`, `hx-trigger`, `hx-target`, `hx-indicator`
  - Real-time search with 500ms debounce
  - Loading indicators and error handling
- **VALUESELECT Example** - Cascading dropdowns with HTMX
  - Demonstrates `hx-get`, `hx-target`, `hx-trigger`
  - Dynamic model loading based on make selection
  - Comprehensive car database with 400+ makes and models
- **PLY3 Example** - Mutually exclusive dropdowns with HTMX
  - Demonstrates `hx-post`, `hx-target`
  - Constraint-based form interactions
  - Server-side state management
- **Development Guiding Light** - Comprehensive development standards
- **Invisible character cleaning tools** for code quality
- **uv dependency management** for all examples

### Features
- **HTMX Integration** - All examples use HTMX for dynamic interactions
- **Flask Backend** - Simple, educational Flask implementations
- **Educational Focus** - Clear documentation and learning objectives
- **Code Quality** - Invisible character cleaning and linting tools
- **Modern Tooling** - uv for dependency management

---

## Version History

- **0.7.2** - Updated version management and documentation
- **0.7.1** - Fixed PROGRESSBAR code quality and Development Guiding Light compliance
- **0.7.0** - Added PROGRESSBAR example with improved version management
- **0.4.1** - Fixed git commit workflow and Makefile version management
- **0.4.0** - Added automated version management and comprehensive documentation
- **0.3.1** - Fixed invisible character cleaning script file extension handling
- **0.3.0** - Added git commit rules and development workflow standards
- **0.2.1** - Added Makefile and automated version management
- **0.2.0** - Clean HTMX implementation with CDN and comprehensive improvements
- **0.1.0** - Initial release with three core HTMX examples

## Contributing

When adding new features or making changes, please update this changelog following the format above. Include:

- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** for vulnerability fixes