import pytest
from Prime_Supplements.models import Product, Cart, CartItem
from Prime_Supplements import db

def test_guest_cart_flow(client, init_database):
    """
    Test adding to cart without logging in (Guest).
    """
    product = Product.query.first()
    
    # 1. Add to Cart as Guest
    # Session ID should be generated automatically
    response = client.get(f'/add_to_cart/{product.id}', follow_redirects=True)
    assert response.status_code == 200
    # Should redirect to login? Or allow guest cart? 
    # Checking cart/routes.py implied current_user.is_authenticated check
    # If not authenticated, it uses session.get('session_id')
    
    # Verify we are on login page OR cart page depending on implementation.
    # Looking at route source in memory (from previous turns):
    # It creates a guest cart linked to session_id.
    assert b"Test Vitamin" in response.data
    
    # 2. Verify Session persistence
    # Subsequent requests should keep the items
    response = client.get('/Cart')
    assert b"Test Vitamin" in response.data

def test_search_functionality(client, init_database):
    """
    Test Search in Shop.
    """
    # 1. Search for existing
    response = client.get('/Shop?search=Test', follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Vitamin" in response.data
    
    # 2. Search for non-existing
    response = client.get('/Shop?search=NonExistentThing', follow_redirects=True)
    assert response.status_code == 200
    assert b"Test Vitamin" not in response.data
    # Maybe check for "No products found" message if it exists in template
