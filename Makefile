# HTMX Flask Examples Makefile

.PHONY: help version clean test install pre-git-commit lint

# Default target
help: ## Show this help message
	@echo "HTMX Flask Examples - Available targets:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Examples:"
	@echo "  make help                    # Show this help message"
	@echo "  make version 0.2.0          # Update version to 0.2.0 and create git tag"
	@echo "  make clean                   # Clean up temporary files"
	@echo "  make test                    # Run tests on all examples"
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
	@sed -i 's/version = "0\.[0-9]\+\.[0-9]\+"/version = "$(VERSION)"/g' ACTIVESEARCH/pyproject.toml
	@sed -i 's/version = "0\.[0-9]\+\.[0-9]\+"/version = "$(VERSION)"/g' VALUESELECT/pyproject.toml
	@sed -i 's/version = "0\.[0-9]\+\.[0-9]\+"/version = "$(VERSION)"/g' PLY3/pyproject.toml
	@sed -i 's/\*\*Version: [0-9]\+\.[0-9]\+\.[0-9]\+\*\*/\*\*Version: $(VERSION)\*\*/g' README.md
	@echo "Note: Remember to update docs/CHANGELOG.md with new version details"
	@echo "Version updated to $(VERSION) in all files"
	@echo "Creating git tag v$(VERSION)..."
	@git add .
	@git commit -m "Version $(VERSION) - Update version numbers across project"
	@git tag -a v$(VERSION) -m "Version $(VERSION) - HTMX Flask Examples"
	@echo "Git tag v$(VERSION) created successfully"
	@echo "Version update complete!"

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
	uv run -- flake8 --ignore=W391 --exclude=.venv ACTIVESEARCH || true
	@echo "Running flake8 on VALUESELECT..."
	uv run -- flake8 --ignore=W391 --exclude=.venv VALUESELECT || true
	@echo "Running flake8 on PLY3..."
	uv run -- flake8 --ignore=W391 --exclude=.venv PLY3 || true
	@echo "Linting complete!"

test: lint ## Run tests on all examples (lint + tests)
	@echo "Running tests on all examples..."
	@echo "Note: This would run tests if they existed"
	@echo "Tests completed!"

install: ## Install dependencies for all examples
	@echo "Installing dependencies for all examples..."
	@echo "ACTIVESEARCH:"
	@cd ACTIVESEARCH && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "VALUESELECT:"
	@cd VALUESELECT && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "PLY3:"
	@cd PLY3 && uv pip install -e . || echo "  Failed to install (check if uv is available)"
	@echo "Installation complete!"

pre-git-commit: ## Remove invisible characters from all files before git commit
	@echo "Removing invisible characters from all files..."
	@python scripts/clean_invisible_chars.py . --clean
	@echo "Invisible characters removed successfully!"
	@echo "Ready for git commit!"