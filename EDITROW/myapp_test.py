#!/usr/bin/env python3
"""
Test file for HTMX Edit Row Example
"""

import pytest
from myapp import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Edit Row Example' in response.data
    assert b'Manny Pacquiao' in response.data
    assert b'Nonito Donaire' in response.data


def test_get_contact(client):
    """Test getting a specific contact."""
    response = client.get('/contact/1')
    assert response.status_code == 200
    assert b'Manny Pacquiao' in response.data
    assert b'manny@pacquiao.com' in response.data


def test_get_nonexistent_contact(client):
    """Test getting a contact that doesn't exist."""
    response = client.get('/contact/999')
    assert response.status_code == 404


def test_edit_contact_form(client):
    """Test getting the edit form for a contact."""
    response = client.get('/contact/1/edit')
    assert response.status_code == 200
    assert b'input' in response.data
    assert b'Manny Pacquiao' in response.data
    assert b'manny@pacquiao.com' in response.data


def test_update_contact(client):
    """Test updating a contact."""
    data = {'name': 'Manny Updated', 'email': 'manny.updated@pacquiao.com'}
    response = client.put('/contact/1', data=data)
    assert response.status_code == 200
    assert b'Manny Updated' in response.data
    assert b'manny.updated@pacquiao.com' in response.data


def test_update_nonexistent_contact(client):
    """Test updating a contact that doesn't exist."""
    data = {'name': 'Test', 'email': 'test@example.com'}
    response = client.put('/contact/999', data=data)
    assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__])
