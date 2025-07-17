#!/usr/bin/env python3
"""
Invisible Character Detector and Cleaner

Detects and removes invisible/problematic characters that commonly appear
in AI-generated code and documentation.
"""

import sys
from pathlib import Path
from typing import List, Tuple, Dict, Optional

# Common problematic invisible characters
INVISIBLE_CHARS = {
    '\u200B': 'Zero Width Space',
    '\u200C': 'Zero Width Non-Joiner',
    '\u200D': 'Zero Width Joiner',
    '\u2060': 'Word Joiner',
    '\uFEFF': 'Byte Order Mark (BOM)',
    '\u00A0': 'Non-Breaking Space',
    '\u2000': 'En Quad',
    '\u2001': 'Em Quad',
    '\u2002': 'En Space',
    '\u2003': 'Em Space',
    '\u2004': 'Three-Per-Em Space',
    '\u2005': 'Four-Per-Em Space',
    '\u2006': 'Six-Per-Em Space',
    '\u2007': 'Figure Space',
    '\u2008': 'Punctuation Space',
    '\u2009': 'Thin Space',
    '\u200A': 'Hair Space',
    '\u202F': 'Narrow No-Break Space',
    '\u205F': 'Medium Mathematical Space',
    '\u3000': 'Ideographic Space',
    # Smart quotes that should be regular quotes in code
    '\u2018': 'Left Single Quotation Mark',
    '\u2019': 'Right Single Quotation Mark',
    '\u201C': 'Left Double Quotation Mark',
    '\u201D': 'Right Double Quotation Mark',
    # Em/En dashes that should be hyphens in code
    '\u2013': 'En Dash',
    '\u2014': 'Em Dash',
}

# Binary/image file extensions to skip
BINARY_EXTENSIONS = {
    '.svg', '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico', '.webp',
    '.lock', '.zip', '.tar', '.gz', '.rar', '.7z', '.exe', '.dll', '.so',
    '.dylib', '.bin', '.dat', '.db', '.sqlite', '.sqlite3'
}


def detect_invisible_chars(content: str) -> List[Tuple[int, int, str, str]]:
    """
    Detect invisible characters in content.

    Returns:
        List of (line_num, char_pos, character, description) tuples
    """
    issues = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        for char_pos, char in enumerate(line):
            if char in INVISIBLE_CHARS:
                issues.append((line_num, char_pos, char,
                                INVISIBLE_CHARS[char]))

    return issues


def clean_content(content: str) -> Tuple[str, Dict[str, int]]:
    """
    Clean invisible characters from content.

    Returns:
        (cleaned_content, replacement_counts)
    """
    cleaned = content
    replacements = {}

    # Replace problematic characters
    for char, description in INVISIBLE_CHARS.items():
        count = cleaned.count(char)
        if count > 0:
            replacements[description] = count

            # Smart replacements
            if char in ['\u2018', '\u2019']:  # Smart single quotes
                cleaned = cleaned.replace(char, "'")
            elif char in ['\u201C', '\u201D']:  # Smart double quotes
                cleaned = cleaned.replace(char, '"')
            elif char in ['\u2013', '\u2014']:  # Em/En dashes
                cleaned = cleaned.replace(char, '-')
            elif char == '\u00A0':  # Non-breaking space
                cleaned = cleaned.replace(char, ' ')
            else:  # Remove other invisible characters
                cleaned = cleaned.replace(char, '')

    return cleaned, replacements


def should_process_file(file_path: Path, extensions: List[str]) -> bool:
    """
    Determine if a file should be processed for invisible character cleaning.

    Args:
        file_path: Path to the file to check
        extensions: List of file extensions to process

    Returns:
        True if file should be processed, False otherwise
    """
    # Skip if not a file
    if not file_path.is_file():
        return False

    # Skip binary/image files
    if file_path.suffix.lower() in BINARY_EXTENSIONS:
        return False

    # Skip build/cache directories
    skip_dirs = ['.venv', '.git', 'node_modules', '.pytest_cache',
                 '__pycache__', '.mypy_cache', 'htmlcov', 'dist',
                 'build', '.eggs', '.tox']
    if any(part in file_path.parts for part in skip_dirs):
        return False

    # Check if file has extension in our list OR is a known file without extension
    known_files_without_ext = ['LICENSE', 'VERSION', 'Makefile']
    return (file_path.suffix.lower() in extensions or
            file_path.name in known_files_without_ext)


def get_processable_files(directory: Path, extensions: List[str]) -> List[Path]:
    """
    Get all files that should be processed for invisible character cleaning.

    Args:
        directory: Directory to scan
        extensions: List of file extensions to process

    Returns:
        List of file paths that should be processed
    """
    return [file_path for file_path in directory.rglob('*')
            if should_process_file(file_path, extensions)]


def scan_file(file_path: Path) -> Tuple[List[Tuple[int, int, str, str]], bool]:
    """
    Scan a single file for invisible characters.

    Returns:
        (issues_found, is_text_file)
    """
    try:
        # Try to read as text
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = detect_invisible_chars(content)
        return issues, True

    except (UnicodeDecodeError, PermissionError):
        # Skip binary files or files we can't read
        return [], False


def clean_file(file_path: Path, dry_run: bool = True) -> bool:
    """
    Clean invisible characters from a file.

    Returns:
        True if file was modified, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        cleaned_content, replacements = clean_content(original_content)

        if cleaned_content != original_content:
            print(f"🔧 {file_path}")
            for desc, count in replacements.items():
                print(f"   - Removed {count} × {desc}")

            if not dry_run:
                # Create backup
                backup_path = file_path.with_suffix(file_path.suffix + '.bak')
                with open(backup_path, 'w', encoding='utf-8') as f:
                    f.write(original_content)
                print(f"   - Backup created: {backup_path}")

                # Write cleaned content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)
                print(f"   - File cleaned successfully")

            return True

        return False

    except Exception as e:
        print(f"❌ Error processing {file_path}: {e}")
        return False


def scan_directory(directory: Path, extensions: Optional[List[str]] = None) -> None:
    """
    Scan directory for invisible characters.
    """
    if extensions is None:
        extensions = ['.py', '.md', '.txt', '.json', '.toml', '.css', '.html',
                     '.cursorrules', '.csv', '.yml', '.yaml']

    print(f"🔍 Scanning {directory} for invisible characters...")
    print(f"📁 File types: {', '.join(extensions)}")
    print()

    total_files = 0
    files_with_issues = 0
    total_issues = 0

    for file_path in get_processable_files(directory, extensions):
        total_files += 1
        issues, is_text = scan_file(file_path)

        if issues:
            files_with_issues += 1
            total_issues += len(issues)
            print(f"⚠️  {file_path}")

            # Show first 5
            for line_num, char_pos, char, description in issues[:5]:
                print(f"   Line {line_num}, Char {char_pos}: " +
                f"{description} (\\u{ord(char):04X})")

            if len(issues) > 5:
                print(f"   ... and {len(issues) - 5} more issues")
            print()

    print("📊 SUMMARY:")
    print(f"   Files scanned: {total_files}")
    print(f"   Files with issues: {files_with_issues}")
    print(f"   Total issues found: {total_issues}")


def main():
    """Main function with CLI interface."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Detect and clean invisible characters in files"
    )
    parser.add_argument('path', help='File or directory to process')
    parser.add_argument('--clean', action='store_true',
                       help='Clean files (creates .bak backups)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be cleaned without making changes')
    parser.add_argument('--extensions', nargs='+',
                       default=['.py', '.md', '.txt', '.json', '.toml', '.css', '.html', '.cursorrules', '.csv', '.yml', '.yaml'],
                       help='File extensions to process')

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"❌ Path does not exist: {path}")
        sys.exit(1)

    if path.is_file():
        # Process single file
        print(f"🔍 Scanning {path}...")
        issues, is_text = scan_file(path)

        if not is_text:
            print("❌ File is not a text file or cannot be read")
            sys.exit(1)

        if issues:
            print(f"⚠️  Found {len(issues)} invisible character issues:")
            for line_num, char_pos, char, description in issues:
                print(f"   Line {line_num}, Char {char_pos}: {description} (\\u{ord(char):04X})")

            if args.dry_run:
                print("\n🔍 DRY RUN MODE - Would clean these issues (no changes made)")
            elif args.clean:
                print()
                clean_file(path, dry_run=False)
        else:
            print("✅ No invisible characters found")

    else:
        # Process directory
        if args.dry_run:
            print("🔍 DRY RUN MODE - Showing what would be cleaned")
            print("   (No files will be modified)")
            print()

            # Scan all files and show what would be cleaned
            for file_path in get_processable_files(path, args.extensions):
                print(f"🔍 Would scan: {file_path}")
                issues, is_text = scan_file(file_path)
                if is_text and issues:
                    print(f"   ⚠️  Would clean {len(issues)} issues")
                    for line_num, char_pos, char, description in issues:
                        print(f"      Line {line_num}, Char {char_pos}: {description}")
        elif args.clean:
            print("🔧 CLEANING MODE - Files will be modified!")
            print("   (Backups will be created with .bak extension)")
            print("   Proceeding automatically...")
            print()

            # Clean all files (no prompting - assume yes)
            for file_path in get_processable_files(path, args.extensions):
                clean_file(file_path, dry_run=False)
        else:
            # Just scan
            scan_directory(path, args.extensions)


if __name__ == '__main__':
    main()