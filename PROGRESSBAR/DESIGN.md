# HTMX Progress Bar Example: Design & Implementation

## Overview
This example demonstrates a real-time progress bar using HTMX with Flask. The implementation follows the official HTMX progress bar pattern from https://htmx.org/examples/progress-bar/.

## Architecture

### Key Components
- **Flask Backend**: Handles task initiation, progress tracking, and completion
- **HTMX Frontend**: Manages real-time updates without JavaScript
- **Global Progress State**: Simple in-memory progress tracking (5% increments)

### Endpoints
- `GET /` - Main page with start button
- `POST /job/start` - Initiates task and returns progress bar HTML
- `GET /job/progress` - Returns current progress (5% increments)
- `GET /job/done` - Returns completion message

## Implementation Details

### 1. Main Page (`/`)
```html
<button class="btn primary" hx-post="/job/start">
    Start server side task
</button>
```

### 2. Task Initiation (`POST /job/start`)
- Resets global `PROGRESS` to 0
- Returns progress bar HTML with self-polling div
- Uses `hx-trigger="done"` to handle completion

### 3. Progress Updates (`GET /job/progress`)
- Increments `PROGRESS` by 5% each call
- Returns updated progress bar HTML
- Sends `HX-Trigger: done` header when progress reaches 100%

### 4. Completion (`GET /job/done`)
- Returns simple completion message
- Triggered by HTMX when `HX-Trigger: done` is received

## HTMX Pattern

### Self-Polling Progress Bar
The progress bar HTML includes a self-polling div that updates itself:

```html
<div hx-trigger="done" hx-get="/job/done" hx-swap="outerHTML" hx-target="this">
    <h3 role="status" id="pblabel" tabindex="-1" autofocus>Running</h3>

    <div hx-get="/job/progress"
         hx-trigger="every 600ms"
         hx-target="this"
         hx-swap="innerHTML">
        <div class="progress" role="progressbar"
             aria-valuemin="0" aria-valuemax="100"
             aria-valuenow="0" aria-labelledby="pblabel">
            <div id="pb" class="progress-bar" style="width:0%"></div>
        </div>
    </div>
</div>
```

### How It Works
1. **Start**: Button triggers `/job/start`, returns progress bar with polling div
2. **Polling**: Inner div polls `/job/progress` every 600ms, updates progress bar
3. **Completion**: When progress reaches 100%, server sends `HX-Trigger: done`
4. **Done**: Outer div triggers `/job/done`, replaces entire progress bar with completion message

## Detailed Walkthrough: Stages and API Calls

### Stage 1: Initial Page Load
**API Call:** `GET /`

**Server Response:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Progress Bar - HTMX Example</title>
  <script src="https://unpkg.com/htmx.org@2.0.3/dist/htmx.min.js"></script>
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Progress Bar</h1>
    <div hx-target="this" hx-swap="outerHTML">
        <h3>Start Progress</h3>
        <button class="btn primary" hx-post="/job/start">
                  Start server side task
        </button>
    </div>
</body>
</html>
```

**Browser State:**
- Page loads with start button
- HTMX library loaded and ready
- Button configured to POST to `/job/start` and replace its container

### Stage 2: User Clicks "Start server side task"
**API Call:** `POST /job/start`

**Server Action:**
- Resets global `PROGRESS` variable to 0
- Returns progress bar HTML with self-polling mechanism

**Server Response:**
```html
<div hx-trigger="done" hx-get="/job/done" hx-swap="outerHTML" hx-target="this">
    <h3 role="status" id="pblabel" tabindex="-1" autofocus>Running</h3>

    <div hx-get="/job/progress"
         hx-trigger="every 600ms"
         hx-target="this"
         hx-swap="innerHTML">
        <div class="progress" role="progressbar" aria-valuemin="0"
        aria-valuemax="100" aria-valuenow="0" aria-labelledby="pblabel">
            <div id="pb" class="progress-bar" style="width:0%"></div>
        </div>
    </div>
</div>
```

**HTMX Action:**
- Replaces the button container with progress bar HTML
- Inner div starts polling `/job/progress` every 600ms
- Outer div listens for "done" event to trigger completion

**Browser State:**
- Button disappears, progress bar appears
- Progress bar shows 0% with "Running" status
- Polling begins automatically

### Stage 3: First Progress Update (5%)
**API Call:** `GET /job/progress`

**Server Action:**
- Increments `PROGRESS` from 0 to 5
- Returns updated progress bar HTML

**Server Response:**
```html
<div class="progress" role="progressbar" aria-valuemin="0"
aria-valuemax="100" aria-valuenow="5" aria-labelledby="pblabel">
  <div id="pb" class="progress-bar" style="width:5%"></div>
</div>
```

**HTMX Action:**
- Replaces inner div content with updated progress bar
- Progress bar now shows 5% completion
- Polling continues every 600ms

**Browser State:**
- Progress bar updates to 5%
- "Running" status remains visible
- Polling continues

### Stage 4: Multiple Progress Updates (10%, 15%, 20%, etc.)
**API Calls:** `GET /job/progress` (repeated every 600ms)

**Server Action:**
- Increments `PROGRESS` by 5% each call: 10%, 15%, 20%, 25%, etc.
- Returns updated progress bar HTML each time

**Server Response (example for 25%):**
```html
<div class="progress" role="progressbar" aria-valuemin="0"
aria-valuemax="100" aria-valuenow="25" aria-labelledby="pblabel">
  <div id="pb" class="progress-bar" style="width:25%"></div>
</div>
```

**HTMX Action:**
- Progress bar smoothly updates every 600ms
- Visual progress increases in 5% increments
- Polling continues until completion

**Browser State:**
- Progress bar animates from 5% → 10% → 15% → 20% → 25% → ...
- "Running" status remains visible
- Smooth visual progress indication

### Stage 5: Near Completion (95% → 100%)
**API Call:** `GET /job/progress` (when PROGRESS = 95)

**Server Action:**
- Increments `PROGRESS` from 95 to 100
- Returns final progress bar HTML
- **Sends `HX-Trigger: done` header**

**Server Response:**
```html
<div class="progress" role="progressbar" aria-valuemin="0"
aria-valuemax="100" aria-valuenow="100" aria-labelledby="pblabel">
  <div id="pb" class="progress-bar" style="width:100%"></div>
</div>
```

**HTTP Headers:**
```
HX-Trigger: done
```

**HTMX Action:**
- Progress bar shows 100% completion
- `HX-Trigger: done` header triggers the outer div's "done" event
- Outer div automatically calls `/job/done`

**Browser State:**
- Progress bar reaches 100%
- "Running" status still visible
- Completion event triggered

### Stage 6: Task Completion
**API Call:** `GET /job/done` (triggered by "done" event)

**Server Action:**
- Returns completion message

**Server Response:**
```html
<h2>Task completed!</h2>
```

**HTMX Action:**
- Replaces entire progress bar container with completion message
- Polling stops (no more polling div in DOM)
- Task is complete

**Browser State:**
- Progress bar disappears
- "Task completed!" message appears
- No more polling or updates

## API Call Summary

| Stage | API Call | Method | Purpose | Response |
|-------|----------|--------|---------|----------|
| 1 | `/` | GET | Load initial page | HTML with start button |
| 2 | `/job/start` | POST | Start task | Progress bar HTML with polling |
| 3-19 | `/job/progress` | GET | Update progress | Progress bar HTML (5% increments) |
| 20 | `/job/progress` | GET | Final update | Progress bar HTML + `HX-Trigger: done` |
| 21 | `/job/done` | GET | Complete task | Completion message |

## Key HTMX Attributes Explained

### Outer Div (Completion Handler)
```html
<div hx-trigger="done" hx-get="/job/done" hx-swap="outerHTML" hx-target="this">
```
- `hx-trigger="done"`: Listens for "done" event (from `HX-Trigger` header)
- `hx-get="/job/done"`: Calls completion endpoint when triggered
- `hx-swap="outerHTML"`: Replaces entire div with response
- `hx-target="this"`: Targets the div itself

### Inner Div (Progress Polling)
```html
<div hx-get="/job/progress" hx-trigger="every 600ms" hx-target="this" hx-swap="innerHTML">
```
- `hx-get="/job/progress"`: Calls progress endpoint
- `hx-trigger="every 600ms"`: Polls every 600 milliseconds
- `hx-target="this"`: Targets the div itself
- `hx-swap="innerHTML"`: Replaces only inner content, preserves polling div

## Key Features

### Accessibility
- Proper ARIA attributes (`aria-valuemin`, `aria-valuemax`, `aria-valuenow`)
- Status role and focus management
- Screen reader friendly progress indication

### Bootstrap Styling
- Uses Bootstrap-style progress bar classes
- Responsive design
- Clean, modern appearance

### Error Handling
- Simple global state management
- Graceful completion handling
- No complex task queuing or persistence

## Testing

The implementation includes comprehensive unit tests that verify:
- Endpoint functionality
- Progress increments (5% steps)
- HTML structure validation
- CSS class presence
- Completion handling

## Limitations

### Current Implementation
- Single global progress state (not suitable for multiple concurrent tasks)
- In-memory storage (progress lost on server restart)
- No error recovery or retry logic
- Simple 5% increment simulation

### Production Considerations
- Use database or Redis for progress storage
- Implement task queuing (Celery, RQ)
- Add error handling and retry logic
- Support multiple concurrent tasks
- Add authentication and authorization

## Files Structure
```
PROGRESSBAR/
├── myapp.py              # Flask application
├── myapp_test.py         # Unit tests
├── templates/
│   └── index.html        # Main page template
├── static/
│   └── css/
│       └── style.css     # Custom styles
└── DESIGN.md             # This file
```

## Usage

### Development
```bash
cd PROGRESSBAR
uv run python myapp.py
```

### Testing
```bash
uv run python myapp_test.py
```

### Access
Open http://localhost:5000 in your browser and click "Start server side task" to see the progress bar in action.