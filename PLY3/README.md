# PLY3 Example

## HTMX Features Demonstrated
- Primary: `hx-post`, `hx-target`

## User Story
As a user, I want to update select options dynamically so that I can make dependent choices.

## How It Works
1. User changes a select box
2. HTMX sends a POST request to `/callback/<n>`
3. Server returns updated select boxes reflecting the new state
4. HTMX replaces the select row with the new HTML

## Try It Out
1. `cd PLY3`
2. Install [uv](https://github.com/astral-sh/uv) if you haven't already: `pip install uv`
3. Install dependencies: `uv pip install -r requirements.txt` or `uv venv && uv pip install .`
4. Run the server: `uv venv && source .venv/bin/activate && python myapp.py`
5. Visit http://localhost:5000

**Note:** This project now uses [uv](https://github.com/astral-sh/uv) for dependency management as the standard for all examples.

## Learning Points
- Demonstrates dependent select boxes with HTMX
- Shows how to update multiple elements from the server
- Example of server-driven UI state 