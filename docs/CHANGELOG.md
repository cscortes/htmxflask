# Changelog

All notable changes to the HTMX Flask Examples project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2024-12-19

### Added
- **Git Commit Rules** in `.cursorrules` for consistent development workflow
  - Mandatory version bumping before commits using `make version VERSION=x.x.x`
  - Required documentation updates (README.md, docs/CHANGELOG.md, etc.)
  - Proper change documentation and versioning requirements
- **Development Workflow Standards** to ensure project consistency

## [0.3.1] - 2024-12-19

### Fixed
- **Invisible character cleaning script** - Improved file extension handling
  - Added support for all project file types (`.css`, `.html`, `.cursorrules`, `.csv`, `.yml`, `.yaml`)
  - Added support for files without extensions (`LICENSE`, `VERSION`, `Makefile`)
  - Excluded binary/image files (`.svg`, `.lock`, `.png`, `.jpg`, etc.) from processing
  - Excluded `.venv` directories and other build/cache directories
  - Refactored extension logic into reusable functions (`should_process_file`, `get_processable_files`)
  - Eliminated code duplication and improved maintainability

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
  - Updated all examples to use `https://unpkg.com/htmx.org@2.0.6/dist/htmx.min.js`
  - Simplified project structure by removing empty js directories
- **ACTIVESEARCH Example**:
  - Added proper HTML structure with DOCTYPE and head section
  - Created comprehensive CSS with HTMX indicators and responsive design
  - Added error handling for no results
  - Enhanced documentation with detailed HTMX pattern explanation
  - Added 24 diverse users with Hispanic names and randomized emails
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