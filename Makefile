# HTMX Flask Examples Makefile

.PHONY: help version version-update clean test test-example install pre-git-commit lint test-files

# Default target
help: ## Show this help message
	@echo "HTMX Flask Examples - Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make help                    # Show this help message"
	@echo "  make version-update TYPE=feature  # Auto-bump version for new features"
	@echo "  make version-update TYPE=bugfix   # Auto-bump version for bug fixes"
	@echo "  make version 0.2.0          # Update version to 0.2.0 and create git tag"
	@echo "  make clean                   # Clean up temporary files"
	@echo "  make test                    # Run tests on all examples"
	@echo "  make test-example EXAMPLE=CLICKEDIT  # Run tests for specific example"
	@echo "  make test-files              # Run all _test.py files in project"
	@echo "  make install                 # Install dependencies for all examples"
	@echo "  make pre-git-commit          # Remove invisible characters before commit"

version: ## Update version to specified version (e.g., make version 0.2.0)
	@if [ -z "$(VERSION)" ]; then \
		echo "Error: Please specify a version number"; \
		echo "Usage: make version VERSION=0.2.0"; \
		exit 1; \
	fi
	@echo "Updating version to $(VERSION)..."
	@echo "$(VERSION)" > VERSION
	@echo "Reading version from VERSION file and updating all pyproject.toml files..."
	@VERSION_FROM_FILE=$$(cat VERSION); \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' ACTIVESEARCH/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' VALUESELECT/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' PLY3/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' PROGRESSBAR/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' CLICKEDIT/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' CLICKLOAD/pyproject.toml; \
	sed -i 's/\*\*Version: [0-9]\+\.[0-9]\+\.[0-9]\+\*\*/\*\*Version: '$$VERSION_FROM_FILE'\*\*/g' README.md
	@echo "Note: Remember to update docs/CHANGELOG.md with new version details"
	@echo "Version updated to $(VERSION) in all files"
	@echo "Creating git tag v$(VERSION)..."
	@git add .
	@git commit -m "Version $(VERSION) - Update version numbers across project"
	@git tag -a v$(VERSION) -m "Version $(VERSION) - HTMX Flask Examples"
	@echo "Git tag v$(VERSION) created successfully"
	@echo "Version update complete!"

version-update: ## Automatically bump version based on change type (make version-update TYPE=feature|bugfix|patch)
	@if [ -z "$(TYPE)" ]; then \
		echo "Error: Please specify change type"; \
		echo "Usage: make version-update TYPE=feature|bugfix|patch"; \
		echo "  feature: bump minor version (0.1.0 -> 0.2.0)"; \
		echo "  bugfix:  bump patch version (0.1.0 -> 0.1.1)"; \
		echo "  patch:   bump patch version (0.1.0 -> 0.1.1)"; \
		exit 1; \
	fi
	@echo "Determining current version..."
	@if [ ! -f VERSION ]; then \
		echo "Error: VERSION file not found. Please run 'make version VERSION=0.1.0' first."; \
		exit 1; \
	fi
	@CURRENT_VERSION=$$(cat VERSION); \
	echo "Current version: $$CURRENT_VERSION"; \
	MAJOR=$$(echo $$CURRENT_VERSION | cut -d. -f1); \
	MINOR=$$(echo $$CURRENT_VERSION | cut -d. -f2); \
	PATCH=$$(echo $$CURRENT_VERSION | cut -d. -f3); \
	if [ "$(TYPE)" = "feature" ]; then \
		NEW_MINOR=$$((MINOR + 1)); \
		NEW_VERSION="$$MAJOR.$$NEW_MINOR.0"; \
		echo "Feature change: bumping minor version to $$NEW_VERSION"; \
	elif [ "$(TYPE)" = "bugfix" ] || [ "$(TYPE)" = "patch" ]; then \
		NEW_PATCH=$$((PATCH + 1)); \
		NEW_VERSION="$$MAJOR.$$MINOR.$$NEW_PATCH"; \
		echo "Bug fix: bumping patch version to $$NEW_VERSION"; \
	else \
		echo "Error: Invalid TYPE. Use 'feature', 'bugfix', or 'patch'"; \
		exit 1; \
	fi; \
	echo "Updating version to $$NEW_VERSION..."; \
	echo "$$NEW_VERSION" > VERSION; \
	echo "Reading version from VERSION file and updating all pyproject.toml files..."; \
	VERSION_FROM_FILE=$$(cat VERSION); \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' ACTIVESEARCH/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' VALUESELECT/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' PLY3/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' PROGRESSBAR/pyproject.toml; \
	sed -i 's/version = "[^"]*"/version = "'$$VERSION_FROM_FILE'"/g' CLICKEDIT/pyproject.toml; \
	sed -i 's/\*\*Version: [0-9]\+\.[0-9]\+\.[0-9]\+\*\*/\*\*Version: '$$VERSION_FROM_FILE'\*\*/g' README.md; \
	echo "Version updated to $$NEW_VERSION in all files"; \
	echo "Note: Remember to update docs/CHANGELOG.md with new version details"

clean: ## Clean up temporary files and build artifacts
	@echo "Cleaning up temporary files..."
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.bak" -delete
	@find . -name ".venv" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "uv.lock" -delete
	@echo "Cleanup complete!"

lint: ## Run flake8 linter on all examples
	@echo "Installing flake8 in the environment..."
	uv pip install flake8 > /dev/null
	@echo "Running flake8 on ACTIVESEARCH..."
	uv run -- flake8 --ignore=W391,E128 --exclude=.venv ACTIVESEARCH 2>/dev/null || true
	@echo "Running flake8 on VALUESELECT..."
	uv run -- flake8 --ignore=W391,E128 --exclude=.venv VALUESELECT 2>/dev/null || true
	@echo "Running flake8 on PLY3..."
	uv run -- flake8 --ignore=W391,E128 --exclude=.venv PLY3 2>/dev/null || true
	@echo "Running flake8 on PROGRESSBAR..."
	uv run -- flake8 --ignore=W391,E128 --exclude=.venv PROGRESSBAR 2>/dev/null || true
	@echo "Running flake8 on CLICKEDIT..."
	uv run -- flake8 --ignore=W391,E128 --exclude=.venv CLICKEDIT 2>/dev/null || true
	@echo "Running flake8 on CLICKLOAD..."
	uv run -- flake8 --ignore=W391,E128 --exclude=.venv CLICKLOAD 2>/dev/null || true
	@echo "Linting complete!"

test: lint ## Run tests on all examples (lint + tests)
	@echo "Running tests on all examples..."
	@echo "Running tests on ACTIVESEARCH..."
	@cd ACTIVESEARCH && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Running tests on VALUESELECT..."
	@cd VALUESELECT && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Running tests on PLY3..."
	@cd PLY3 && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Running tests on PROGRESSBAR..."
	@cd PROGRESSBAR && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Running tests on CLICKEDIT..."
	@cd CLICKEDIT && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Running tests on CLICKLOAD..."
	@cd CLICKLOAD && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Tests completed!"

test-example: ## Run tests for a specific example (make test-example EXAMPLE=CLICKEDIT)
	@if [ -z "$(EXAMPLE)" ]; then \
		echo "Error: Please specify an example name"; \
		echo "Usage: make test-example EXAMPLE=CLICKEDIT"; \
		echo "Available examples: ACTIVESEARCH, VALUESELECT, PLY3, PROGRESSBAR, CLICKEDIT, CLICKLOAD"; \
		exit 1; \
	fi
	@echo "Running tests for $(EXAMPLE)..."
	@cd $(EXAMPLE) && (test -f myapp_test.py && uv run python myapp_test.py 2>/dev/null > /tmp/test_output 2>&1 && echo "  ✓ Tests passed" || echo "  ✗ Tests failed") || echo "  No test file found"
	@echo "Tests for $(EXAMPLE) completed!"

test-files: ## Run all _test.py files found in the project
	@echo "Finding and running all _test.py files..."
	@find . -name "*_test.py" -type f | while read file; do \
		echo "Running $$file..."; \
		cd $$(dirname $$file) && uv run python $$(basename $$file) 2>/dev/null || echo "  Tests failed"; \
		cd - > /dev/null; \
	done
	@echo "All _test.py files completed!"

install: ## Install dependencies for all examples
	@echo "Installing dependencies for all examples..."
	@echo "ACTIVESEARCH:"
	@cd ACTIVESEARCH && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "VALUESELECT:"
	@cd VALUESELECT && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "PLY3:"
	@cd PLY3 && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "PROGRESSBAR:"
	@cd PROGRESSBAR && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "CLICKEDIT:"
	@cd CLICKEDIT && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "CLICKLOAD:"
	@cd CLICKLOAD && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "Installation complete!"

pre-git-commit: ## Remove invisible characters from all files before git commit
	@echo "Removing invisible characters from all files..."
	@python scripts/clean_invisible_chars.py . --clean
	@echo "Invisible characters removed successfully!"
	@echo "Ready for git commit!"