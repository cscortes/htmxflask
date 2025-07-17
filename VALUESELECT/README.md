# VALUESELECT Example

## HTMX Features Demonstrated
- Primary: `hx-get`, `hx-target`

## User Story
As a user, I want to select a car make and see available models so that I can choose the right car.

## How It Works
1. User selects a car make from the dropdown
2. HTMX sends a GET request to `/models/` with the selected make
3. Server returns a list of models for that make
4. HTMX updates the models dropdown with the new options

## Try It Out
1. `cd VALUESELECT`
2. `pipenv install`
3. `pipenv run python myapp.py`
4. Visit http://localhost:5000

## Learning Points
- Demonstrates dynamic dropdowns with HTMX
- Shows how to use server data to drive UI updates
- Example of minimal Flask + HTMX integration 