# ACTIVESEARCH Example

## HTMX Features Demonstrated
- Primary: `hx-post`, `hx-trigger`, `hx-target`
- Secondary: `hx-indicator`

## User Story
As a user, I want to search contacts as I type so that I can quickly find people.

## How It Works
1. User types in the search box
2. HTMX sends a POST request to `/search/` on each keyup (with delay)
3. Server returns a filtered HTML fragment of matching users
4. HTMX replaces the table body with the results

## Try It Out
1. `cd ACTIVESEARCH`
2. `pipenv install`
3. `pipenv run python myapp.py`
4. Visit http://localhost:5000

## Learning Points
- Demonstrates live search pattern with HTMX
- Shows how to use loading indicators
- Example of progressive enhancement
- Minimal Flask backend logic 