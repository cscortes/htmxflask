# PLY3 Example

## HTMX Features Demonstrated
- **Primary**: `hx-post`, `hx-target`
- **Secondary**: Server-side state management

## User Story
As a user, I want to select from three interdependent dropdowns where only one can have a value at a time, so that I can make mutually exclusive choices.

## How It Works
1. User selects a value in any of the three dropdowns
2. HTMX sends a POST request to `/callback/<dropdown_number>` with the new selection
3. Server processes the selection and ensures mutual exclusion (only one dropdown can have a value)
4. Server returns updated HTML for all three dropdowns with correct `selected` states
5. HTMX replaces the entire row (`#idx_row`) with the new state

## HTMX Pattern Explained
This example demonstrates **mutually exclusive dropdowns**:
- **`hx-post="/callback/<n>"`**: Sends POST request when dropdown changes
- **`hx-target="#idx_row"`**: Replaces the entire row containing all dropdowns
- **Server-side constraint logic**: Ensures only one dropdown can be selected at a time
- **State synchronization**: All dropdowns are updated to reflect the current selection

## Try It Out
1. `cd PLY3`
2. Install [uv](https://github.com/astral-sh/uv) if you haven't already: `pip install uv`
3. Install dependencies: `uv pip install -r requirements.txt` or `uv venv && uv pip install .`
4. Run the server: `uv run myapp.py`
5. Visit http://localhost:5000

**Note:** This project now uses [uv](https://github.com/astral-sh/uv) for dependency management as the standard for all examples.

## Learning Points
- **Mutual Exclusion**: How to implement constraint-based form interactions
- **Server-side State Management**: Handling complex form logic on the server
- **HTML Fragment Updates**: Replacing multiple elements with a single server response
- **Error Handling**: Safe handling of form data and validation
- **Template-based Responses**: Using Jinja2 templates for dynamic HTML generation

## Key Differences from VALUESELECT
- **VALUESELECT**: Cascading dropdowns (selecting one populates another)
- **PLY3**: Mutually exclusive dropdowns (selecting one deselects others)

## Code Structure
```
PLY3/
├── myapp.py              # Flask routes with constraint logic
├── templates/
│   └── index.html        # Main page with interdependent dropdowns
├── static/
│   └── assets/
│       └── css/          # Bootstrap and custom styling
└── pyproject.toml        # Dependencies
```