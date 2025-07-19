# HTMX Progress Bar Example

This example demonstrates how to create a real-time progress bar using
HTMX and Flask. It simulates a long-running task and shows progress
updates in real-time.

**Based on the working HTMX example at: https://htmx.org/examples/progress-bar/**

## Features

- **Real-time Progress Updates**: Progress bar updates every 600ms
during task execution
- **Simple State Management**: Uses global progress variable for easy demonstration
- **HTMX Integration**: Leverages HTMX for seamless UI updates without JavaScript
- **Responsive Design**: Clean, modern interface with Bootstrap-style progress bar
- **Accessibility**: Proper ARIA attributes for screen readers
- **Self-Polling Pattern**: Demonstrates correct HTMX progress bar implementation

## How It Works

### HTMX Implementation

1. **Task Initiation**: Uses `hx-post="/job/start"` to initiate a new task
2. **Progress Polling**: HTMX polls the server every 600ms for progress updates
3. **Dynamic Updates**: Progress bar updates in real-time with 5% increments
4. **Completion Handling**: Automatic completion when progress reaches 100%

### Server-Side Processing

- **Task Start**: Resets global progress to 0 and returns progress bar HTML
- **Progress Updates**: Increments progress by 5% each poll request
- **Completion**: Sends `HX-Trigger: done` header when progress reaches 100%
- **HTML API**: Returns HTML fragments for direct DOM updates

## Key HTMX Patterns Demonstrated

- `hx-post`: Initiating server-side actions
- `hx-target`: Targeting specific DOM elements for updates
- `hx-swap`: Controlling how content is inserted
- `hx-trigger`: Setting up automatic polling with `every 600ms`
- `HX-Trigger`: Server-side event triggering for completion

## Critical HTMX Pattern: Self-Polling Progress Bar

This example demonstrates the correct pattern for HTMX progress bars:

```html
<!-- Initial state -->
<div hx-target="this" hx-swap="outerHTML">
    <h3>Start Progress</h3>
    <button class="btn primary" hx-post="/job/start">Start server side task</button>
</div>

<!-- Progress state (returned by /job/start) -->
<div hx-trigger="done" hx-get="/job/done" hx-swap="outerHTML" hx-target="this">
    <h3 role="status" id="pblabel" tabindex="-1" autofocus>Running</h3>

    <div hx-get="/job/progress" hx-trigger="every 600ms" hx-target="this" hx-swap="innerHTML">
        <div class="progress" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0" aria-labelledby="pblabel">
            <div id="pb" class="progress-bar" style="width:0%"></div>
        </div>
    </div>
</div>
```

**Key Points:**
- The progress bar container polls itself (`hx-target="this"`)
- Progress updates replace only the progress bar content (`hx-swap="innerHTML"`)
- The outer container handles completion state changes (`hx-trigger="done"`)
- No JavaScript required - pure HTMX

## Installation & Running

1. **Install Dependencies**:
   ```bash
   uv sync
   ```

2. **Run the Application**:
   ```bash
   uv run python myapp.py
   ```

3. **Access the Example**:
   Open your browser to `http://localhost:5000`

4. **Run Tests**:
   ```bash
   uv run python myapp_test.py
   ```

## Code Structure

```
PROGRESSBAR/
├── myapp.py              # Flask application with progress logic
├── myapp_test.py         # Unit tests for the implementation
├── templates/
│   └── index.html        # Main interface with HTMX implementation
├── static/
│   └── css/
│       └── style.css     # Bootstrap-style progress bar CSS
├── pyproject.toml        # Project dependencies
├── DESIGN.md             # Detailed design documentation
└── README.md             # This file
```

## API Endpoints

- `GET /`: Main page with progress bar interface
- `POST /job/start`: Initiates a new task, returns progress bar HTML
- `GET /job/progress`: Returns updated progress bar HTML (5% increments)
- `GET /job/done`: Returns completion message

## Implementation Details

### Flask Routes

- **`/` (GET)**: Serves the main page with start button
- **`/job/start` (POST)**: Creates a new task and returns the progress bar HTML
- **`/job/progress` (GET)**: Returns current progress as HTML fragment
- **`/job/done` (GET)**: Returns completion message

### Progress Processing

The progress system:
- Uses a global `PROGRESS` variable for simple state management
- Increments progress by 5% each poll request
- Takes approximately 12 seconds to complete (20 steps × 600ms)
- Sends `HX-Trigger: done` header when progress reaches 100%

### HTMX Integration

- Uses `hx-trigger="every 600ms"` for smooth progress updates
- Leverages CSS transitions for smooth visual updates
- Implements proper accessibility attributes (`aria-valuenow`, etc.)
- Uses `HX-Trigger` header for completion signaling

## Testing

The implementation includes comprehensive unit tests that verify:
- Endpoint functionality and responses
- Progress increments (5% steps)
- HTML structure validation
- CSS class presence
- Completion handling

Run tests with:
```bash
uv run python myapp_test.py
```

## Customization

### Changing Progress Increments
Modify the increment value in the `/job/progress` route:
```python
PROGRESS = 100 if PROGRESS >= 100 else PROGRESS + 5  # Change 5 to desired increment
```

### Changing Polling Frequency
Modify the `hx-trigger` attribute in the progress bar HTML:
```html
<div hx-get="/job/progress" hx-trigger="every 600ms" ...>  <!-- Change 600ms -->
```

### Adding Real Tasks
Replace the simple increment with actual work:
```python
@app.route('/job/progress')
def job_progress():
    global PROGRESS
    # Your actual work here
    PROGRESS = calculate_real_progress()

    html = f'<div class="progress">...</div>'
    response = make_response(html)
    if PROGRESS >= 100:
        response.headers['HX-Trigger'] = 'done'
    return response
```

### Styling
The progress bar uses Bootstrap-style CSS that can be customized in `static/css/style.css`.

## Browser Compatibility

This example works in all modern browsers that support:
- HTMX 2.0+
- CSS3 transitions

## Learning Objectives

- Understanding HTMX self-polling patterns
- Implementing server-side progress tracking
- Creating responsive progress indicators
- Managing state in web applications
- Server-side HTML generation for dynamic content
- Using `HX-Trigger` headers for event signaling

## Troubleshooting

### Common Issues

1. **Port Already in Use**: If port 5000 is busy, change the port in `myapp.py`
2. **HTMX Not Loading**: Ensure the HTMX script is properly loaded from CDN
3. **Progress Not Updating**: Check browser console for JavaScript errors
4. **Tests Failing**: Ensure all dependencies are installed with `uv sync`

### Debug Mode

The Flask app runs in debug mode by default, which provides:
- Automatic reloading on code changes
- Detailed error messages
- Debug console access

## Related Documentation

- [DESIGN.md](DESIGN.md) - Detailed design documentation and walkthrough
- [HTMX Progress Bar Example](https://htmx.org/examples/progress-bar/) - Official HTMX example
- [HTMX Documentation](https://htmx.org/docs/) - Complete HTMX reference