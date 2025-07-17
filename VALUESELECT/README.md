# VALUESELECT Example

## HTMX Features Demonstrated
- **Primary**: `hx-get`, `hx-target`, `hx-trigger`
- **Secondary**: `hx-indicator`

## User Story
As a user, I want to select a car make and see available models so that I can choose the right car configuration.

## How It Works
1. User selects a car make from the first dropdown
2. HTMX sends a GET request to `/models/` with the selected make as a query parameter
3. Server returns an HTML fragment containing `<option>` elements for that make's models
4. HTMX replaces the content of the models dropdown with the new options
5. Loading indicator shows during the request for better user experience

## HTMX Pattern Explained
This example demonstrates the **cascading dropdown** pattern:
- **`hx-get="/models/"`**: Sends GET request to fetch model data
- **`hx-target="#ddmodels"`**: Replaces content in the models dropdown
- **`hx-trigger="change"`**: Triggers when the make selection changes
- **`hx-indicator=".htmx-indicator"`**: Shows loading feedback during request

## Try It Out
1. `cd VALUESELECT`
2. Install [uv](https://github.com/astral-sh/uv) if you haven't already: `pip install uv`
3. Install dependencies: `uv pip install -r requirements.txt` or `uv venv && uv pip install .`
4. Run the server: `uv venv && source .venv/bin/activate && python myapp.py`
5. Visit http://localhost:5000

**Note:** This project now uses [uv](https://github.com/astral-sh/uv) for dependency management as the standard for all examples.

## Learning Points
- **Cascading Dropdowns**: How to create dependent dropdowns with HTMX
- **HTML Fragments**: Server returns partial HTML that gets swapped into the page
- **Loading States**: Using `hx-indicator` to show feedback during requests
- **Error Handling**: Graceful handling of invalid selections and missing data
- **Minimal JavaScript**: Pure HTMX solution with no custom JavaScript needed

## Data Source
The example uses a comprehensive car database (`car.csv`) with over 400 car makes and models from around the world, including:
- American brands (Ford, Chevrolet, Cadillac)
- European brands (BMW, Audi, Mercedes-Benz)
- Asian brands (Toyota, Honda, Hyundai)
- Luxury brands (Bentley, Aston Martin, Rolls-Royce)

### Sample Data Retrieval Script
The `getdata.py` script demonstrates how to scrape car data from Wikipedia to create the `car.csv` file:

```bash
# Install data retrieval dependencies
uv pip install -e ".[data-retrieval]"

# Run the sample script to fetch fresh data
python getdata.py
```

This script:
- Scrapes SUV data from Wikipedia's "List of sport utility vehicles" page
- Extracts make and model information from HTML tables
- Creates a properly formatted CSV file for the HTMX example
- Shows how to integrate external data sources into HTMX applications

## Code Structure
```
VALUESELECT/
├── myapp.py              # Flask routes and data loading
├── templates/
│   └── index.html        # Main page with HTMX dropdowns
├── static/
│   ├── css/
│   │   └── style.css     # Styling and HTMX indicators
│   └── js/
│       └── htmx.js       # HTMX library
├── car.csv               # Car make-model database
├── getdata.py            # Sample data retrieval script
└── pyproject.toml        # Dependencies
``` 