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
2. Install [uv](https://github.com/astral-sh/uv) if you haven't already: `pip install uv`
3. Install dependencies: `uv pip install -r requirements.txt` or `uv venv && uv pip install .`
4. Run the server: `uv venv && source .venv/bin/activate && python myapp.py`
5. Visit http://localhost:5000

**Note:** This project now uses [uv](https://github.com/astral-sh/uv) for dependency management as the standard for all examples.

## Learning Points
- Demonstrates dynamic dropdowns with HTMX
- Shows how to use server data to drive UI updates
- Example of minimal Flask + HTMX integration 