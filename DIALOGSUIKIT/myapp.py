#!/usr/bin/env python3

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key in production

# In-memory storage for form submissions
submissions = []

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://unpkg.com; style-src 'self' https://unpkg.com; object-src 'none';"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/')
def index():
    """Render the main page with UIKit modal examples"""
    return render_template('index.html', submissions=submissions)

@app.route('/modal')
def modal():
    """Return the modal dialog HTML"""
    return render_template('modal.html')

@app.route('/submit', methods=['POST'])
def submit():
    """Handle form submission from modal"""
    name = request.form.get('name', '').strip()
    
    if name:
        submissions.append({
            'name': name,
            'timestamp': 'Just now'
        })
        return f"Hello, {name}! Your submission has been saved."
    else:
        return "Please enter your name."

@app.route('/clear', methods=['POST'])
def clear():
    """Clear all submissions"""
    submissions.clear()
    return "All submissions cleared!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
