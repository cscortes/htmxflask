#!/usr/bin/env python3
"""
HTMX Inline Validation Example

This example demonstrates real-time form field validation using HTMX patterns:
- hx-post: Send validation requests to server
- hx-trigger="input": Trigger validation on user input with debouncing
- hx-target: Update specific validation message elements
- hx-indicator: Show validation loading states

Based on the official HTMX inline-validation example.
Follows Development Guiding Light principles for educational clarity.
"""

import os
import re
import time
from flask import Flask, render_template, request, jsonify

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
static_dir = os.path.join(os.path.dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# Mock database of existing usernames
TAKEN_USERNAMES = {
    'admin', 'root', 'user', 'test', 'demo', 'guest',
    'administrator', 'system', 'webmaster', 'support'
}

# Password strength requirements
PASSWORD_REQUIREMENTS = {
    'min_length': 8,
    'uppercase': True,
    'lowercase': True,
    'digits': True,
    'special_chars': True
}


@app.route('/')
def index():
    """Main page with validation form."""
    return render_template('index.html')


@app.route('/validate/username', methods=['POST'])
def validate_username():
    """Validate username field with availability check."""
    time.sleep(0.2)  # Simulate server processing delay

    username = request.form.get('username', '').strip()

    if not username:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Username is required')

    if len(username) < 3:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Username must be at least 3 characters')

    if len(username) > 20:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Username cannot exceed 20 characters')

    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return render_template('validation_message.html',
                             field_type='error',
                             message='Username can only contain letters, numbers, and underscores')

    if username.lower() in TAKEN_USERNAMES:
        return render_template('validation_message.html',
                             field_type='error',
                             message='This username is already taken')

    return render_template('validation_message.html',
                         field_type='success',
                         message='Username is available')


@app.route('/validate/email', methods=['POST'])
def validate_email():
    """Validate email field with format checking."""
    time.sleep(0.15)  # Simulate server processing delay

    email = request.form.get('email', '').strip()

    if not email:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Email is required')

    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return render_template('validation_message.html',
                             field_type='error',
                             message='Please enter a valid email address')

    # Basic domain validation (check for common domains)
    domain = email.split('@')[1].lower()
    common_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com']

    if domain in common_domains:
        return render_template('validation_message.html',
                             field_type='success',
                             message='Valid email address')
    else:
        return render_template('validation_message.html',
                             field_type='warning',
                             message='Email accepted (please verify domain)')


@app.route('/validate/password', methods=['POST'])
def validate_password():
    """Validate password field with strength checking."""
    time.sleep(0.1)  # Simulate server processing delay

    password = request.form.get('password', '')

    if not password:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Password is required')

    if len(password) < PASSWORD_REQUIREMENTS['min_length']:
        return render_template('validation_message.html',
                             field_type='error',
                             message=f'Password must be at least {PASSWORD_REQUIREMENTS["min_length"]} characters')

    strength_score = 0
    messages = []

    if re.search(r'[A-Z]', password):
        strength_score += 1
    else:
        messages.append('Add uppercase letter')

    if re.search(r'[a-z]', password):
        strength_score += 1
    else:
        messages.append('Add lowercase letter')

    if re.search(r'\d', password):
        strength_score += 1
    else:
        messages.append('Add number')

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        strength_score += 1
    else:
        messages.append('Add special character')

    if strength_score >= 3:
        return render_template('validation_message.html',
                             field_type='success',
                             message='Strong password')
    elif strength_score >= 2:
        return render_template('validation_message.html',
                             field_type='warning',
                             message='Medium strength - ' + ', '.join(messages[:2]))
    else:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Weak password - ' + ', '.join(messages))


@app.route('/validate/confirm-password', methods=['POST'])
def validate_confirm_password():
    """Validate confirm password field by comparing with original password."""
    time.sleep(0.1)  # Simulate server processing delay

    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if not confirm_password:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Please confirm your password')

    if confirm_password != password:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Passwords do not match')

    return render_template('validation_message.html',
                         field_type='success',
                         message='Passwords match')


@app.route('/validate/age', methods=['POST'])
def validate_age():
    """Validate age field with numeric and range checking."""
    time.sleep(0.1)  # Simulate server processing delay

    age_str = request.form.get('age', '').strip()

    if not age_str:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Age is required')

    if not age_str.isdigit():
        return render_template('validation_message.html',
                             field_type='error',
                             message='Age must be a number')

    try:
        age = int(age_str)
        if age < 13:
            return render_template('validation_message.html',
                                 field_type='error',
                                 message='Must be at least 13 years old')
        elif age > 120:
            return render_template('validation_message.html',
                                 field_type='error',
                                 message='Age cannot exceed 120 years')
        elif age < 18:
            return render_template('validation_message.html',
                                 field_type='warning',
                                 message='Some features may be restricted for users under 18')
        else:
            return render_template('validation_message.html',
                                 field_type='success',
                                 message='Age verified')
    except ValueError:
        return render_template('validation_message.html',
                             field_type='error',
                             message='Invalid age format')


@app.route('/submit-form', methods=['POST'])
def submit_form():
    """Handle complete form submission with final validation."""
    time.sleep(0.3)  # Simulate processing delay

    # Collect all form data
    form_data = {
        'username': request.form.get('username', '').strip(),
        'email': request.form.get('email', '').strip(),
        'password': request.form.get('password', ''),
        'confirm_password': request.form.get('confirm_password', ''),
        'age': request.form.get('age', '').strip()
    }

    errors = []
    warnings = []

    # Validate all fields
    if not form_data['username']:
        errors.append('Username is required')
    elif len(form_data['username']) < 3:
        errors.append('Username too short')

    if not form_data['email']:
        errors.append('Email is required')
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', form_data['email']):
        errors.append('Invalid email format')

    if not form_data['password']:
        errors.append('Password is required')
    elif len(form_data['password']) < 8:
        errors.append('Password too short')

    if form_data['password'] != form_data['confirm_password']:
        errors.append('Passwords do not match')

    if not form_data['age']:
        errors.append('Age is required')
    elif not form_data['age'].isdigit() or int(form_data['age']) < 13:
        errors.append('Invalid age')

    if errors:
        return jsonify({
            'success': False,
            'message': 'Please fix the following errors:',
            'errors': errors
        })

    return jsonify({
        'success': True,
        'message': 'Registration successful! Welcome aboard.',
        'data': {
            'username': form_data['username'],
            'email': form_data['email']
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
