# Release Checklist

This document provides a comprehensive checklist for creating releases of the HTMX Flask Examples project. Follow this checklist to ensure consistent, high-quality releases.

## 🎯 Release Types

### Feature Release (Minor Version Bump)
- **When**: New HTMX examples, major functionality additions
- **Version**: `0.19.0` → `0.20.0`
- **Command**: `make version-update TYPE=feature`

### Bug Fix Release (Patch Version Bump)
- **When**: Bug fixes, documentation updates, minor improvements
- **Version**: `0.19.0` → `0.19.1`
- **Command**: `make version-update TYPE=patch`

### Major Release (Major Version Bump)
- **When**: Breaking changes, major architectural changes
- **Version**: `0.19.0` → `1.0.0`
- **Command**: `make version-update TYPE=major`

## 📋 Pre-Release Checklist

### Code Quality
- [ ] **All tests pass**: `make test`
- [ ] **Code is linted**: `make lint`
- [ ] **No linting errors**: Check flake8 output
- [ ] **Invisible characters cleaned**: `python scripts/clean_invisible_chars.py . --clean`
- [ ] **Code follows Development Guiding Light principles**
- [ ] **CSS is minimal** (< 50 lines for basic examples)
- [ ] **JavaScript is minimal** (ideally 0 lines beyond HTMX)

### Documentation
- [ ] **README.md updated** with new features
- [ ] **CHANGELOG.md updated** with new version entry
- [ ] **FEATURES.md updated** with completion status
- [ ] **Example READMEs updated** (if applicable)
- [ ] **DESIGN.md files updated** (if applicable)
- [ ] **All documentation is accurate and complete**

### Testing
- [ ] **Unit tests pass** for all examples
- [ ] **Integration tests pass**
- [ ] **Manual testing completed** for new features
- [ ] **Cross-browser testing** (if applicable)
- [ ] **Accessibility testing** (if applicable)
- [ ] **Performance testing** (if applicable)

### Project Structure
- [ ] **All examples follow consistent structure**
- [ ] **pyproject.toml files are updated** with new version
- [ ] **Makefile includes new examples** (if applicable)
- [ ] **Dependencies are up to date**

### GitHub Issue Management
- [ ] **Check if release resolves any open issues**: `gh issue list --state open`
- [ ] **Identify specific issues resolved** by this release
- [ ] **Close resolved issues** with detailed completion comments
- [ ] **Update issue labels** (if applicable)
- [ ] **Link issues to releases** in commit messages
- [ ] **Create new issues** for future work (if applicable)
- [ ] **Verify issue closure** after release: `gh issue view ISSUE_NUMBER`

## 🚀 Release Process

### Step 1: Prepare for Release
```bash
# 1. Ensure you're on the main branch
git checkout main
git pull origin main

# 2. Run all tests
make test

# 3. Clean invisible characters
python scripts/clean_invisible_chars.py . --clean

# 4. Update documentation (if not already done)
# - Update README.md
# - Update CHANGELOG.md
# - Update FEATURES.md
```

### Step 2: Version Bump
```bash
# Choose appropriate version type
make version-update TYPE=feature    # For new features
make version-update TYPE=patch      # For bug fixes
make version-update TYPE=major      # For breaking changes
```

### Step 3: Final Verification
```bash
# 1. Verify version was updated correctly
cat VERSION

# 2. Run tests one more time
make test

# 3. Check that all pyproject.toml files were updated
grep -r "version = " */pyproject.toml
```

### Step 4: Commit Changes
```bash
# 1. Add all changes
git add .

# 2. Commit with descriptive message
git commit -m "feat: Add FEATURE_NAME example with DESCRIPTION

Features:
- FEATURE_NAME: Brief description
- Additional features or improvements
- Bug fixes and enhancements

Examples: X/47 completed (Y%)
HTMX Patterns: hx-get, hx-post, hx-target, hx-swap"
```

### Step 5: GitHub Issue Management
```bash
# 1. Check if any open issues are resolved by this release
gh issue list --state open

# 2. Identify specific issues resolved (look for matching feature names)
# Example: If implementing "DIALOGSUIKIT", look for "Dialogs - UIKit" issues

# 3. Close resolved issues with detailed comments
VERSION=$(cat VERSION)
gh issue close ISSUE_NUMBER --comment "✅ **COMPLETED in v$VERSION**

This feature has been successfully implemented with the FEATURE_NAME example:

## Implementation Details:
- **Directory**: FEATURE_NAME/
- **HTMX Patterns**: hx-pattern1, hx-pattern2, hx-pattern3
- **Features**: 
  - Feature description 1
  - Feature description 2
  - X comprehensive unit tests
  - Educational documentation
  - Security-compliant implementation

## Technical Highlights:
- All X tests passing
- Minimal CSS following Development Guiding Light principles
- Security headers and proper error handling
- Based on official HTMX example: https://htmx.org/examples/...

## Files Created:
- FEATURE_NAME/myapp.py - Flask application
- FEATURE_NAME/templates/index.html - Main page
- FEATURE_NAME/templates/modal.html - Modal content (if applicable)
- FEATURE_NAME/static/css/style.css - Enhanced styling
- FEATURE_NAME/myapp_test.py - Test suite
- FEATURE_NAME/README.md - Documentation
- FEATURE_NAME/DESIGN.md - Design decisions

The example is fully functional, tested, and ready for production use! 🚀"

# 4. Verify issues are closed
gh issue view ISSUE_NUMBER

# 5. Check final issue status
gh issue list --state closed --limit 5
```

### Step 6: Create Git Tag
```bash
# 1. Create annotated tag
VERSION=$(cat VERSION)
git tag -a $VERSION -m "Release $VERSION: FEATURE_NAME

Features:
- FEATURE_NAME: Brief description
- Additional features or improvements
- Bug fixes and enhancements

Examples: X/47 completed (Y%)
HTMX Patterns: hx-get, hx-post, hx-target, hx-swap"

# 2. Push changes and tag
git push origin main
git push origin $VERSION
```

### Step 7: Automated Release (Alternative)
```bash
# Use the automated release command
make release TYPE=feature
```

## 📝 Release Message Templates

### Feature Release
```bash
git tag -a v0.20.0 -m "Release v0.20.0: Add RESETINPUT example with security-compliant JavaScript

Features:
- RESETINPUT example demonstrating automatic form input reset
- Event listener approach to avoid htmx:evalDisallowedError
- 24 comprehensive unit tests covering all functionality
- Minimal CSS following Development Guiding Light principles
- Educational documentation with troubleshooting guide
- Security-compliant JavaScript implementation

Examples: 14/47 completed (29.8%)
HTMX Patterns: hx-on::after-request, hx-post, hx-target, hx-swap"
```

### Bug Fix Release
```bash
git tag -a v0.19.1 -m "Release v0.19.1: Fix client-side validation bug in FILEUPLOADPRESERVE

Fixes:
- Fixed client-side validation preventing server-side validation demonstration
- Removed required and type='email' attributes to allow server-side validation
- Updated unit tests to reflect validation changes
- Improved error handling and user feedback

Examples: 13/47 completed (27.7%)
HTMX Patterns: hx-preserve, hx-post, hx-target, hx-swap"
```

### Major Release
```bash
git tag -a v1.0.0 -m "Release v1.0.0: Complete HTMX Examples Collection

Features:
- All 47 official HTMX examples implemented
- Comprehensive test suite with 500+ tests
- Complete documentation and educational materials
- Production-ready examples with security best practices
- Community contribution guidelines and processes

Examples: 47/47 completed (100%)
HTMX Patterns: All major HTMX attributes and patterns covered"
```

## 🔍 Post-Release Verification

### GitHub Release
- [ ] **Tag was pushed successfully** to GitHub
- [ ] **GitHub release was created** automatically
- [ ] **Release notes are complete** and accurate
- [ ] **Release is marked as latest** (if applicable)

### Documentation Links
- [ ] **Release URL is accessible**: `https://github.com/cscortes/htmxflask/releases/tag/v0.20.0`
- [ ] **Version badges are updated** (if applicable)
- [ ] **Documentation links work** correctly

### Community Notification
- [ ] **GitHub issues are updated** with release information
- [ ] **Resolved issues are properly closed** with completion comments
- [ ] **Issue status is verified**: `gh issue view ISSUE_NUMBER`
- [ ] **Community is notified** (if applicable)
- [ ] **Social media announcements** (if applicable)

## 📊 Release Metrics

### Track These Metrics
- **Examples completed**: X/47 (Y%)
- **Test coverage**: X tests passing
- **Documentation coverage**: All examples documented
- **Community contributions**: X contributors
- **GitHub stars**: X stars
- **Issues resolved**: X issues closed

### Version History
```bash
# View all tags
git tag -l --sort=-version:refname

# Compare versions
git diff v0.19.0..v0.20.0

# Show tag details
git show v0.20.0
```

## 🚨 Emergency Procedures

### Hotfix Release
If a critical bug is found after release:

1. **Create hotfix branch**:
   ```bash
   git checkout -b hotfix/v0.20.1
   ```

2. **Fix the bug** and test thoroughly

3. **Create patch release**:
   ```bash
   make version-update TYPE=patch
   git add .
   git commit -m "fix: Critical bug fix description"
   git tag -a v0.20.1 -m "Hotfix v0.20.1: Critical bug fix"
   git push origin main
   git push origin v0.20.1
   ```

### Rollback Procedure
If a release needs to be rolled back:

1. **Revert the commit**:
   ```bash
   git revert <commit-hash>
   ```

2. **Create rollback release**:
   ```bash
   make version-update TYPE=patch
   git tag -a v0.20.2 -m "Rollback v0.20.2: Revert problematic changes"
   git push origin main
   git push origin v0.20.2
   ```

## 🔧 GitHub Issue Management Automation

### Quick Issue Check Commands
```bash
# Check all open issues
gh issue list --state open

# Check issues by feature type
gh issue list --search "modal OR dialog" --state open
gh issue list --search "validation OR form" --state open
gh issue list --search "upload OR file" --state open

# Check recently closed issues
gh issue list --state closed --limit 5

# View specific issue details
gh issue view ISSUE_NUMBER
```

### Issue Resolution Template
When closing issues, use this standardized template:

```bash
VERSION=$(cat VERSION)
gh issue close ISSUE_NUMBER --comment "✅ **COMPLETED in v$VERSION**

This feature has been successfully implemented with the FEATURE_NAME example:

## Implementation Details:
- **Directory**: FEATURE_NAME/
- **HTMX Patterns**: hx-pattern1, hx-pattern2, hx-pattern3
- **Features**: 
  - Feature description 1
  - Feature description 2
  - X comprehensive unit tests
  - Educational documentation
  - Security-compliant implementation

## Technical Highlights:
- All X tests passing
- Minimal CSS following Development Guiding Light principles
- Security headers and proper error handling
- Based on official HTMX example: https://htmx.org/examples/...

## Files Created:
- FEATURE_NAME/myapp.py - Flask application
- FEATURE_NAME/templates/index.html - Main page
- FEATURE_NAME/static/css/style.css - Enhanced styling
- FEATURE_NAME/myapp_test.py - Test suite
- FEATURE_NAME/README.md - Documentation
- FEATURE_NAME/DESIGN.md - Design decisions

The example is fully functional, tested, and ready for production use! 🚀"
```

### Issue Status Tracking
```bash
# Count open vs closed issues
echo "Open issues: $(gh issue list --state open --json number | jq length)"
echo "Closed issues: $(gh issue list --state closed --json number | jq length)"

# Check issue completion rate
TOTAL_ISSUES=$(gh issue list --json number | jq length)
CLOSED_ISSUES=$(gh issue list --state closed --json number | jq length)
COMPLETION_RATE=$((CLOSED_ISSUES * 100 / TOTAL_ISSUES))
echo "Issue completion rate: $COMPLETION_RATE%"
```

## 📚 Resources

### Documentation
- [Development Guiding Light](DEVGUIDINGLIGHT.md)
- [Changelog](CHANGELOG.md)
- [Features List](../.docs/FEATURES.md)

### Tools
- [Makefile](../Makefile) - Automated release commands
- [Clean Script](../scripts/clean_invisible_chars.py) - Character cleaning
- [GitHub Actions](../.github/workflows/) - CI/CD pipeline

### External Resources
- [Semantic Versioning](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Git Tagging Best Practices](https://git-scm.com/book/en/v2/Git-Basics-Tagging)

## ✅ Quick Release Commands

### Standard Release
```bash
make test && make release TYPE=feature
```

### Manual Release
```bash
make version-update TYPE=feature
git add . && git commit -m "feat: Description"
make create-tag VERSION=$(cat VERSION)
```

### Emergency Hotfix
```bash
# Fix bug, then:
make version-update TYPE=patch
git add . && git commit -m "fix: Critical bug fix"
make create-tag VERSION=$(cat VERSION)
```

### GitHub Issue Management
```bash
# Check and close resolved issues
gh issue list --state open
gh issue close ISSUE_NUMBER --comment "✅ COMPLETED - Feature implemented in v$(cat VERSION)"
gh issue view ISSUE_NUMBER  # Verify closure
```

---

**Remember**: Always test thoroughly before releasing. A bad release is worse than a delayed release!
