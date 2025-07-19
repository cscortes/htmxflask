# HTMX Progress Bar Example: Design & Diagnosis

## Key Assumptions
- **No polling when no task is running**: Polling should only start after a task has been initiated
- **No polling after task completion**: Polling should stop when the task reaches 100%
- **Polling only during active tasks**: The polling element should only be present when a task is actively running

## 1. How HTMX Should Work
- The button in `index.html` uses `hx-post="/start-task"` and `hx-target="#progress-container"`, so the server response replaces the entire `#progress-container` div.
- The server should return a progress bar HTML fragment that includes a polling element (a div with `hx-post="/progress/{task_id}"`, `hx-trigger="every 100ms"`, and `hx-target="#progress-container"`).
- Each poll to `/progress/{task_id}` should return the entire progress bar HTML (with updated progress), including the polling element, so polling continues until the task is complete.
- When the task is complete, the server returns a success message (and no polling element), so polling stops.

## 2. What Was Wrong With the Previous Implementation
- `/progress/<task_id>` returned a `<script>` that tried to update DOM elements, but HTMX expects HTML fragments, not scripts.
- The polling element targeted a separate div, so the DOM was not updated as expected.
- The polling element was not included in the progress update, so polling could stop or not update the right part of the DOM.

## 3. Correct HTMX Pattern (Pseudocode)

**index.html:**
```html
<button hx-post="/start-task" hx-target="#progress-container" hx-swap="innerHTML">Start Task</button>
<div id="progress-container"></div>
```

**/start-task and /progress/<task_id> response:**
```html
<div class="progress-container" style="display: block;">
  <div class="progress-bar">
    <div class="progress-fill" style="width: {{ progress }}%;"></div>
  </div>
  <div class="progress-text">{{ progress }}%</div>
  <div class="progress-message">{{ message }}</div>
</div>
{% if not complete %}
  <div
    hx-post="/progress/{{ task_id }}"
    hx-trigger="every 100ms"
    hx-target="#progress-container"
    hx-swap="innerHTML">
  </div>
{% endif %}
```

**/progress/<task_id> (Python):**
```python
@app.route('/progress/<task_id>', methods=['POST'])
def get_progress(task_id):
    progress = task_progress.get(task_id, 0)
    is_complete = progress >= 100
    message = get_progress_message(progress)
    return render_template_string(PROGRESS_BAR_TEMPLATE, progress=progress, message=message, complete=is_complete, task_id=task_id)
```

## 4. Why This Works
- HTMX replaces the entire `#progress-container` with each poll, so the progress bar and polling element are always in sync.
- When the task is complete, the polling element is omitted, so polling stops.
- No JavaScript is needed; all updates are handled by HTMX and server-rendered HTML.

## 5. Summary Table

| Step                | What HTMX Does                | What Server Returns                | What Gets Replaced         |
|---------------------|-------------------------------|------------------------------------|----------------------------|
| Button click        | POST /start-task              | Progress bar + polling element     | #progress-container        |
| Polling (every 100ms)| POST /progress/<task_id>     | Updated progress bar + polling     | #progress-container        |
| Task complete       | POST /progress/<task_id>      | Success message (no polling)       | #progress-container        |

## 6. Detailed Walkthrough: API Calls and HTML Transformations

### Initial State (Not Started)
**HTML in browser:**
```html
<button hx-post="/start-task" hx-target="#progress-container" hx-swap="innerHTML">Start Task</button>
<div id="progress-container" class="progress-container">
    <!-- Empty -->
</div>
```

### Step 1: User Clicks "Start Task"
**API Call:** `POST /start-task`

**Server Response:**
```html
<div id="progress-container" class="progress-container" style="display: block;">
    <div class="progress-bar">
        <div class="progress-fill" style="width: 0%;"></div>
    </div>
    <div class="progress-text">0%</div>
    <div class="progress-message">Starting task...</div>
    <div hx-post="/progress/task_abc123"
         hx-trigger="every 100ms"
         hx-target="#progress-container"
         hx-swap="innerHTML">
    </div>
</div>
```

**HTMX Action:**
- Replaces `#progress-container` with the response
- Finds the polling div and starts polling every 100ms

### Step 2: First Poll (50% Progress)
**API Call:** `POST /progress/task_abc123`

**Server Response:**
```html
<div id="progress-container" class="progress-container" style="display: block;">
    <div class="progress-bar">
        <div class="progress-fill" style="width: 50%;"></div>
    </div>
    <div class="progress-text">50%</div>
    <div class="progress-message">Processing data...</div>
    <div hx-post="/progress/task_abc123"
         hx-trigger="every 100ms"
         hx-target="#progress-container"
         hx-swap="innerHTML">
    </div>
</div>
```

**HTMX Action:**
- Replaces `#progress-container` with the new response
- **PROBLEM:** The polling div gets destroyed when its parent is replaced
- Polling stops

### Step 3: Task Complete (100%)
**API Call:** `POST /progress/task_abc123`

**Server Response:**
```html
<div class="status success">
    Task completed successfully!
</div>
```

**HTMX Action:**
- Replaces `#progress-container` with the success message
- No polling div in response, so polling stops

### The Root Problem
The polling div is **inside** the target it's trying to replace. When HTMX replaces `#progress-container`, it destroys the polling div that was supposed to continue polling.

### Correct Solution (for reference)
The polling div must be **outside** the target container:

**Correct Start Task Response:**
```html
<div id="progress-container" class="progress-container" style="display: block;">
    <div class="progress-bar">
        <div class="progress-fill" style="width: 0%;"></div>
    </div>
    <div class="progress-text">0%</div>
    <div class="progress-message">Starting task...</div>
</div>
<div hx-post="/progress/task_abc123"
     hx-trigger="every 100ms"
     hx-target="#progress-container"
     hx-swap="innerHTML">
</div>
```

**Correct Progress Response:**
```html
<div id="progress-container" class="progress-container" style="display: block;">
    <div class="progress-bar">
        <div class="progress-fill" style="width: 50%;"></div>
    </div>
    <div class="progress-text">50%</div>
    <div class="progress-message">Processing data...</div>
</div>
```

**Correct Completion Response:**
```html
<div class="status success">
    Task completed successfully!
</div>
```

This way:
- Polling div **stays in place** during updates
- Progress container gets **replaced** with each poll
- Polling **continues** until completion
- At completion, **no polling div** is returned, so polling stops