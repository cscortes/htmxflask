#!/usr/bin/env python3
"""
HTMX Lazy Loading Example

This example demonstrates lazy loading content using HTMX patterns:
- hx-get: Load content on page load
- hx-trigger="load": Trigger request when element is loaded
- hx-indicator: Show loading state during request
- CSS transitions: Smooth fade-in animation using .htmx-settling

Based on the official HTMX lazy-load example.
Follows Development Guiding Light principles for educational clarity.
"""

from flask import Flask, render_template
import time
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Sample data that would be "loaded" lazily
GRAPH_DATA = {
    "title": "Monthly Revenue Analytics",
    "description": "Interactive chart showing revenue trends over the past 12 months",
    "metrics": [
        {"month": "Jan", "revenue": 12500, "growth": "+12%"},
        {"month": "Feb", "revenue": 13200, "growth": "+5.6%"},
        {"month": "Mar", "revenue": 14100, "growth": "+6.8%"},
        {"month": "Apr", "revenue": 13800, "growth": "-2.1%"},
        {"month": "May", "revenue": 15200, "growth": "+10.1%"},
        {"month": "Jun", "revenue": 16800, "growth": "+10.5%"},
        {"month": "Jul", "revenue": 17500, "growth": "+4.2%"},
        {"month": "Aug", "revenue": 18200, "growth": "+4.0%"},
        {"month": "Sep", "revenue": 18900, "growth": "+3.8%"},
        {"month": "Oct", "revenue": 19800, "growth": "+4.8%"},
        {"month": "Nov", "revenue": 21100, "growth": "+6.6%"},
        {"month": "Dec", "revenue": 22500, "growth": "+6.6%"},
    ]
}


@app.route('/')
def index():
    """Main page with lazy loading placeholder."""
    return render_template('index.html')


@app.route('/graph')
def graph():
    """Lazy load endpoint that returns graph content after simulated delay."""
    # Simulate server processing time to demonstrate lazy loading
    time.sleep(1.5)  # 1.5 second delay to show loading effect

    # Prepare data for template
    metrics = GRAPH_DATA['metrics']
    max_revenue = max(m['revenue'] for m in GRAPH_DATA['metrics'])

    # Render template with data
    return render_template('graph.html', metrics=metrics,
                           max_revenue=max_revenue)


if __name__ == '__main__':
    app.run(debug=True)
