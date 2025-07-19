#!/usr/bin/env python3
"""
Progress Bar Example - HTMX Flask Demo

This example demonstrates how to create a progress bar using HTMX.
It simulates a long-running task and updates the progress bar in real-time.
Based on the working HTMX example at https://htmx.org/examples/progress-bar/
"""
from flask import Flask, render_template, make_response


app = Flask(__name__)
PROGRESS=0

@app.route('/')
def index():
    """Main page with progress bar interface."""
    return render_template('index.html')


@app.route('/job/start', methods=['POST'])
def job_start():
    """Start a new task and return progress bar HTML."""
    global PROGRESS
    PROGRESS = 0

    # Return the progress bar HTML that will poll itself
    return '''
        <div hx-trigger="done" hx-get="/job/done" hx-swap="outerHTML"
        hx-target="this">
        <h3 role="status" id="pblabel" tabindex="-1" autofocus>Running</h3>

        <div
            hx-get="/job/progress"
            hx-trigger="every 600ms"
            hx-target="this"
            hx-swap="innerHTML">
            <div class="progress" role="progressbar" aria-valuemin="0"
            aria-valuemax="100" aria-valuenow="0" aria-labelledby="pblabel">
            <div id="pb" class="progress-bar" style="width:0%">
            </div>
        </div>
        </div>
    '''


@app.route('/job/progress')
def job_progress():
    """Get current progress for the active task."""
    global PROGRESS

    PROGRESS = 100 if PROGRESS >= 100 else PROGRESS + 5

    html = f'''
    <div class="progress" role="progressbar" aria-valuemin="0"
    aria-valuemax="100" aria-valuenow="{PROGRESS}" aria-labelledby="pblabel">
      <div id="pb" class="progress-bar" style="width:{PROGRESS}%"></div>
    </div>
    '''

    response = make_response(html)
    if PROGRESS >= 100:
        response.headers['HX-Trigger'] = 'done'
    return response

@app.route('/job/done')
def job():
    return '''
    <h2>Task completed!</h2>
    '''


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
