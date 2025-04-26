from flask import Flask, render_template , redirect, url_for, flash, session
from forms import RegisterForm, LoginForm, CartForm, ReviewForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import uuid

#------------------------------------------------------------------------------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = '123 456 789'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Orders.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

#------------------------------------------------------------------------------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Relationship for template access, if desired
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

#------------------------------------------------------------------------------------------------

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(300))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)

    cart = db.relationship('Cart', backref=db.backref('items', lazy=True))
    product = db.relationship('Product')

#------------------------------------------------------------------------------------------------

with app.app_context():
     db.create_all()

#------------------------------------------------------------------------------------------------

@app.route('/')
@app.route("/Home", methods=['GET','POST'])
def Home():
    return render_template('Home.HTML', title = "Home", cssFile = "Static/css/Home.css")

@app.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "Static/css/About.css")

#------------------------------------------------------------------------------------------------

@app.route('/Reviews', methods=['GET', 'POST'])
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        if 'user_id' not in session:
            flash('You must be logged in to post a review.', 'danger')
            return redirect(url_for('login'))
        review = Review(
            user_id=session['user_id'],
            content=form.content.data.strip(),
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added!', 'success')
        return redirect(url_for('reviews'))
    all_reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('Review.html', form=form, reviews=all_reviews)

@app.route('/reviews/edit/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if 'user_id' not in session:
        flash('You must be logged in to edit reviews.', 'danger')
        return redirect(url_for('login'))
    if review.user_id != session['user_id']:
        flash('You are not allowed to edit this review.', 'danger')
        return redirect(url_for('reviews'))
    form = ReviewForm(obj=review)
    if form.validate_on_submit():
        review.content = form.content.data.strip()
        db.session.commit()
        flash('Review updated!', 'success')
        return redirect(url_for('reviews'))
    return render_template('edit_review.html', form=form, review=review)

@app.route('/reviews/delete/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if 'user_id' not in session:
        flash('You must be logged in to delete reviews.', 'danger')
        return redirect(url_for('login'))
    if review.user_id != session['user_id']:
        flash('You are not allowed to delete this review.', 'danger')
        return redirect(url_for('reviews'))
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'info')
    return redirect(url_for('reviews'))

#------------------------------------------------------------------------------------------------

@app.route("/Shop")
def Shop():
    products = Product.query.all()
    return render_template('Shop.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'user_id' in session:
        user_id = session['user_id']
        cart = Cart.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Cart(user_id=user_id)
            db.session.add(cart)
            db.session.commit()
    else:
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
        if not cart:
            cart = Cart(session_id=session_id)
            db.session.add(cart)
            db.session.commit()

    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('Shop'))

@app.route('/create_products')
def create_products():
    if Product.query.count() == 0:
        products = [
            Product(name="Gut Health+", description="Improve Digestion", price=44.99, image_url="/static/images/GutHealth+.png"),
            Product(name="B Complex", description="Essential B Vitamins", price=44.99, image_url="/static/images/B-Complex.png"),
            Product(name="Fiber", description="Promote Digestive Health", price=44.99, image_url="/static/images/Fiber.png"),
            Product(name="Liver", description="Support Optimal Liver Health", price=44.99, image_url="/static/images/Liver.png"),
            Product(name="Multi Mineral", description="Support Healthy Bones and Joints", price=44.99, image_url="/static/images/MultiMineral.png"),
            Product(name="Multi Vitamin", description="Provide Essential Micronutrients", price=44.99, image_url="/static/images/MultiVitamin.png"),
            Product(name="Thyroid Support", description="Keep Thyroid Operating at Optimal Rate", price=44.99, image_url="/static/images/ThyroidSupport.png"),
            Product(name="Omega 3", description="Support Cardiovascular Health", price=44.99, image_url="/static/images/Omega3.png"),
            ]
        db.session.add_all(products)
        db.session.commit()
        return "Products created!"
    else:
        return "Products already exist!"

@app.route('/Cart')
def CartPage():
    if 'user_id' in session:
        user_id = session['user_id']
        cart = Cart.query.filter_by(user_id=user_id).first()
    elif 'session_id' in session:
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
    else:
        cart = None

    if cart:
        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        total = sum(item.product.price * item.quantity for item in cart_items)
    else:
        cart_items = []
        total = 0.0
    return render_template('Cart.Html', cart_items=cart_items, total=total)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    cart = None
    if 'user_id' in session:
        user_id = session['user_id']
        cart = Cart.query.filter_by(user_id=user_id).first()
    elif 'session_id' in session:
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
    
    if cart:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
    return redirect(url_for('CartPage'))

#------------------------------------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f"Logged in successfully! Welcome {user.username}", "success")
            return redirect(url_for("Home"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template('login.HTML', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data.strip()).first():
            flash("Email already registered. Please log in.", "danger")
            return render_template('signup.HTML', form=form)
        if User.query.filter_by(phone=form.phone.data.strip()).first():
            flash("Phone number already registered. Please log in.", "danger")
            return render_template('signup.HTML', form=form)
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip(),
            phone=form.phone.data.strip(),
            password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("login"))
   return render_template('signup.HTML', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash("Signed out.", "info")
    return redirect(url_for('Home'))
#------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True,port=3000)