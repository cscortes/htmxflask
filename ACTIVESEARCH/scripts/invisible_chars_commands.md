# Invisible Character Detection Commands

This guide provides various methods to detect and remove invisible characters in files, especially useful for AI-generated code and documentation.

## Quick Detection Methods

### 1. Using `cat -A` (Show All Characters)
```bash
# Show all non-printing characters
cat -A filename.py
# $ marks end of lines, ^I shows tabs, etc.

# For multiple files
find src -name "*.py" -exec cat -A {} \; | grep -E '[^\x00-\x7F]'
```

### 2. Using `file` Command (Check Encoding)
```bash
# Check file encoding
file -bi src/lunar_times/cli.py

# Check multiple files
find . -name "*.py" -exec file -bi {} \; | grep -v "us-ascii\|utf-8"
```

### 3. Using `hexdump` (Show Hex Values)
```bash
# Show hex dump to see exact byte values
hexdump -C filename.py | head -20

# Look for suspicious byte patterns
hexdump -C filename.py | grep -E 'c2 a0|e2 80|ef bb bf'
```

### 4. Using `od` (Octal Dump)
```bash
# Show octal/hex dump
od -c filename.py | head -10

# Show just non-ASCII characters
od -c filename.py | grep -E '\\[0-9]{3}'
```

### 5. Using `grep` with Unicode Patterns
```bash
# Find zero-width spaces
grep -P '\u200B' src/**/*.py

# Find non-breaking spaces
grep -P '\u00A0' src/**/*.py

# Find smart quotes
grep -P '[\u2018\u2019\u201C\u201D]' src/**/*.py

# Find em/en dashes
grep -P '[\u2013\u2014]' src/**/*.py

# Find any non-ASCII characters
grep -P '[^\x00-\x7F]' src/**/*.py
```

### 6. Using `iconv` (Character Conversion)
```bash
# Try converting to ASCII (will fail if non-ASCII chars present)
iconv -f utf-8 -t ascii filename.py

# Convert and clean
iconv -f utf-8 -t ascii//IGNORE filename.py > clean_file.py
```

## Common Invisible Characters

| Character | Unicode | Description | Common in AI Code |
|-----------|---------|-------------|-------------------|
| `\u200B` | U+200B | Zero Width Space | ✅ Very Common |
| `\u00A0` | U+00A0 | Non-Breaking Space | ✅ Common |
| `\uFEFF` | U+FEFF | Byte Order Mark (BOM) | ✅ Common |
| `\u2018` | U+2018 | Left Single Quote | ✅ Very Common |
| `\u2019` | U+2019 | Right Single Quote | ✅ Very Common |
| `\u201C` | U+201C | Left Double Quote | ✅ Very Common |
| `\u201D` | U+201D | Right Double Quote | ✅ Very Common |
| `\u2013` | U+2013 | En Dash | ✅ Common |
| `\u2014` | U+2014 | Em Dash | ✅ Common |
| `\u200C` | U+200C | Zero Width Non-Joiner | ⚠️ Occasional |
| `\u200D` | U+200D | Zero Width Joiner | ⚠️ Occasional |

## One-Liner Detection Commands

### Find All Files with Invisible Characters
```bash
# Quick scan of project
find . -name "*.py" -o -name "*.md" -o -name "*.txt" | \
  xargs grep -l -P '[^\x00-\x7F]' | \
  grep -v ".venv"
```

### Find Specific Problem Characters
```bash
# Zero-width spaces (very common)
find src docs tests -name "*.py" -o -name "*.md" | \
  xargs grep -n -P '\u200B'

# Smart quotes (extremely common in AI code)
find src docs tests -name "*.py" -o -name "*.md" | \
  xargs grep -n -P '[\u2018\u2019\u201C\u201D]'

# Non-breaking spaces
find src docs tests -name "*.py" -o -name "*.md" | \
  xargs grep -n -P '\u00A0'
```

### Quick Clean Commands
```bash
# Remove zero-width spaces
sed -i 's/\u200B//g' filename.py

# Replace smart quotes with regular quotes
sed -i 's/[\u2018\u2019]/\'/g' filename.py
sed -i 's/[\u201C\u201D]/"/g' filename.py

# Replace em/en dashes with hyphens
sed -i 's/[\u2013\u2014]/-/g' filename.py

# Replace non-breaking spaces with regular spaces
sed -i 's/\u00A0/ /g' filename.py
```

## Editor-Specific Detection

### VS Code
Add to settings.json:
```json
{
  "editor.renderWhitespace": "all",
  "editor.renderControlCharacters": true,
  "editor.unicodeHighlight.ambiguousCharacters": true,
  "editor.unicodeHighlight.invisibleCharacters": true
}
```

### Vim
```vim
" Show invisible characters
:set list
:set listchars=tab:▸\ ,trail:·,nbsp:⎵

" Highlight problematic Unicode
:syntax match Error /\u200B\|\u00A0\|\u2018\|\u2019\|\u201C\|\u201D/
```

### Emacs
```elisp
;; Show whitespace
(global-whitespace-mode 1)
(setq whitespace-style '(face trailing tabs spaces newline space-mark tab-mark))

;; Highlight Unicode issues
(defface unicode-highlight '((t (:background "red"))) "Face for Unicode issues")
(font-lock-add-keywords 'python-mode '(("[\u200B\u00A0\u2018\u2019\u201C\u201D]" . 'unicode-highlight)))
```

## Prevention Strategies

### 1. Git Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Check for invisible characters before commit
files=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(py|md|txt|json|toml)$')
if [ -n "$files" ]; then
    for file in $files; do
        if grep -P '[^\x00-\x7F]' "$file" > /dev/null; then
            echo "Error: Invisible characters found in $file"
            echo "Run 'make clean-invisible' to fix"
            exit 1
        fi
    done
fi
```

### 2. CI/CD Pipeline Check
Add to your CI workflow:
```yaml
- name: Check for invisible characters
  run: |
    if find src docs tests -name "*.py" -o -name "*.md" | xargs grep -l -P '[^\x00-\x7F]'; then
      echo "Invisible characters detected"
      exit 1
    fi
```

### 3. Editor Configuration
- Enable Unicode highlighting
- Show all whitespace characters
- Use linters that detect encoding issues

## Troubleshooting

### Common Symptoms
- **Syntax errors with "valid" code** → Check for invisible characters
- **String comparison failures** → Zero-width characters in strings
- **Import errors with correct paths** → BOM or invisible chars in filenames
- **Indentation errors in Python** → Mixed spaces/tabs with invisible chars

### Quick Diagnosis
```bash
# Check file encoding
file -bi suspicious_file.py

# Look for non-ASCII in specific line
sed -n '42p' file.py | hexdump -C

# Count invisible characters
grep -o -P '[^\x00-\x7F]' file.py | wc -l
```

## Our Project Tools

### Using Our Python Script
```bash
# Scan for issues (basic check)
make check-invisible

# Detailed scan showing what would be cleaned
make check-invisible-detailed

# Clean files (creates backups, no prompts)
make clean-invisible

# Manual usage
python scripts/clean_invisible_chars.py src                    # Scan only
python scripts/clean_invisible_chars.py src --dry-run         # Show what would be cleaned
python scripts/clean_invisible_chars.py docs --clean          # Clean files (automatic, no prompts)
```

#### Script Options
- **Default**: Scan and report issues only
- **`--dry-run`**: Show detailed analysis of what would be cleaned (no modifications)
- **`--clean`**: Clean files with backup creation (automatic, no user prompts)
- **`--extensions`**: Specify file extensions to process (default: .py, .md, .txt, .json, .toml)

### Integration with Development Workflow
```bash
# Add to your development routine
make lint                     # Check code quality
make check-invisible          # Quick check for invisible chars
make check-invisible-detailed # Detailed invisible char analysis
make lint                     # Run linting
make test-coverage           # Run tests with coverage

# Pre-commit routine
make pre-commit              # Includes invisible char checks
``` 