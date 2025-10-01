#!/usr/bin/env python3

from flask import Flask, render_template, request
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key in production

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
    return render_template('index.html')

@app.route('/modal')
def modal():
    """Return the modal dialog HTML"""
    return render_template('modal.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
