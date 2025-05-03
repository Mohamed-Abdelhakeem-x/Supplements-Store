from Prime_Supplements.Main import main

from Prime_Supplements.models import Product
from Prime_Supplements import bcrypt, db
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid


@main.route('/')
@main.route("/Home", methods=['GET','POST'])
def Home():
    return render_template('Home.HTML', title = "Home", cssFile = "Static/css/Home.css")

@main.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "Static/css/About.css")

@main.route("/Shop")
def Shop():
    search_query = request.args.get('search', '').strip()
    category_filter = request.args.get('category', '').strip()
    
    # Base query
    query = Product.query
    
    # Apply search filter
    if search_query:
        query = query.filter(
            (Product.name.ilike(f'%{search_query}%')) | 
            (Product.description.ilike(f'%{search_query}%'))
        )
    
    # Apply category filter
    if category_filter:
        query = query.filter(Product.category == category_filter)
    
    # Get filtered products
    products = query.all()
    
    # Get unique categories for filter dropdown
    categories = sorted(set(p.category for p in Product.query.all()))
    
    return render_template('Shop.html', products=products, categories=categories, 
                           current_search=search_query, current_category=category_filter)

@main.route('/product/<int:product_id>')
def product_description(product_id):
    product = Product.query.get_or_404(product_id)
    related_products = Product.query.filter(Product.category == product.category).filter(Product.id != product_id).limit(4).all()
    return render_template('product_description.html', product=product, related_products=related_products)
