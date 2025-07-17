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
2. `pipenv install`
3. `pipenv run python myapp.py`
4. Visit http://localhost:5000

## Learning Points
- Demonstrates dependent select boxes with HTMX
- Shows how to update multiple elements from the server
- Example of server-driven UI state 