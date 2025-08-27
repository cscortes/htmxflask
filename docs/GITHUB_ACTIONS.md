# GitHub Actions Workflows

This project uses GitHub Actions for continuous integration, testing, and deployment.

## 📋 Available Workflows

### 1. **CI** (`.github/workflows/ci.yml`)
**Purpose**: Main continuous integration pipeline
**Triggers**:
- Push to main/master branch
- Pull requests to main/master branch

**Features**:
- Runs on Python 3.9 with uv package manager
- Executes `make test` for all examples
- Provides detailed test summary in GitHub UI
- Validates all HTMX patterns and functionality

### 2. **Test Suite** (`.github/workflows/test.yml`)
**Purpose**: Multi-Python version testing
**Triggers**:
- Push to main/master branch
- Pull requests to main/master branch

**Features**:
- Tests on Python 3.9
- Matrix strategy for comprehensive compatibility
- Caches dependencies for faster builds
- Uploads test artifacts for debugging

### 3. **Scheduled Health Check** (`.github/workflows/scheduled.yml`)
**Purpose**: Daily automated health monitoring
**Triggers**:
- Daily at 2 AM UTC (cron schedule)
- Manual trigger via workflow_dispatch

**Features**:
- Ensures project stays healthy over time
- Creates health reports in GitHub UI
- Validates all examples and HTMX patterns
- Early detection of potential issues

### 4. **Deploy Examples** (`.github/workflows/deploy.yml`)
**Purpose**: Deployment automation
**Triggers**:
- Release publication
- Manual trigger with environment selection

**Features**:
- Pre-deployment testing
- Environment-specific deployments (staging/production)
- Deployment package creation
- Comprehensive deployment summaries

## 🚀 How to Use

### Automatic Testing
Workflows run automatically on:
- Every push to main/master branch
- Every pull request
- Daily health checks

### Manual Triggers
You can manually trigger workflows:

1. **Health Check**: Go to Actions → Scheduled Health Check → Run workflow
2. **Deploy**: Go to Actions → Deploy Examples → Run workflow (select environment)

### Viewing Results
- **Actions Tab**: See all workflow runs and results
- **Pull Requests**: CI status appears in PR checks
- **Commit History**: Green checkmarks for passing tests

## 📊 Test Coverage

All workflows validate:

### Examples Tested
- ✅ **ACTIVESEARCH**: Search functionality with HTMX
- ✅ **VALUESELECT**: Cascading dropdowns with data loading
- ✅ **PLY3**: Interdependent dropdowns with mutual exclusion
- ✅ **PROGRESSBAR**: Real-time progress with polling
- ✅ **CLICKEDIT**: Inline editing with form handling
- ✅ **CLICKLOAD**: Lazy loading with pagination
- ✅ **DELETEROW**: Row deletion with animation

### HTMX Patterns Validated
- `hx-get`, `hx-post`, `hx-put` - HTTP methods
- `hx-target`, `hx-swap` - DOM manipulation
- `hx-trigger`, `hx-indicator` - Event handling and loading states
- `hx-delete`, `hx-confirm` - Row deletion and confirmation
- Real-time updates and form validation

## 🔧 Configuration

### Environment Variables
No environment variables required for basic testing.

### Dependencies
- **Python**: 3.9 (matrix testing)
- **Package Manager**: uv (fast Python package management)
- **Testing**: unittest framework
- **Linting**: flake8

### Caching
- **uv dependencies**: Cached for faster builds
- **Test artifacts**: Uploaded for debugging
- **Deployment packages**: Stored for 30 days

## 📈 Monitoring

### Status Badge
Add this badge to your README:
```markdown
![CI](https://github.com/yourusername/htmxflask/workflows/CI/badge.svg)
```

### Health Reports
- Daily health check reports in GitHub UI
- Test summaries for each workflow run
- Deployment summaries with environment details

## 🛠️ Troubleshooting

### Common Issues

1. **Tests Failing**: Check the Actions tab for detailed error logs
2. **Dependency Issues**: Verify pyproject.toml files are correct
3. **Python Version**: Ensure compatibility with tested versions
4. **HTMX Patterns**: Validate HTMX attributes in templates

### Debugging
- Download test artifacts from failed runs
- Check workflow logs for detailed error messages
- Use manual triggers to test specific scenarios

## 🔄 Workflow Dependencies

```
CI ← Main pipeline (fast feedback)
Test Suite ← Multi-version testing
Scheduled ← Health monitoring
Deploy ← Production deployment
```

All workflows use the same `make test` command for consistency.