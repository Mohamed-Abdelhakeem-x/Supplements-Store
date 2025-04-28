from flask import Flask, render_template , redirect, url_for, flash, session
from forms import RegisterForm, LoginForm, CartForm, ReviewForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid

#------------------------------------------------------------------------------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = '123 456 789'

#------------------------------------------------------------------------------------------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Orders.db'
db = SQLAlchemy(app)

#------------------------------------------------------------------------------------------------

bcrypt = Bcrypt(app)

#------------------------------------------------------------------------------------------------

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#------------------------------------------------------------------------------------------------

class User(db.Model, UserMixin):
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
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))

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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#------------------------------------------------------------------------------------------------

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Check if products already exist
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
            print("Database initialized with products!")

# Initialize the database when the application starts
init_db()

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
@login_required
def reviews():
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            title=form.title.data.strip(),
            content=form.content.data.strip(),
        )
        db.session.add(review)
        db.session.commit()
        flash('Review added!', 'success')
        return redirect(url_for('reviews'))
    
    user_reviews = Review.query.filter_by(user_id=current_user.id).order_by(Review.id.desc()).all()
    return render_template('Review.html', form=form, reviews=user_reviews)


@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.user_id != current_user.id:
        flash('You can only edit your own reviews.', 'danger')
        return redirect(url_for('reviews'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review.title = form.title.data.strip()
        review.content = form.content.data.strip()
        db.session.commit()
        flash('Review updated!', 'success')
        return redirect(url_for('reviews'))
    
    form.title.data = review.title
    form.content.data = review.content
    return render_template('Edit_Review.html', form=form, review=review)


@app.route('/reviews/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    if review.user_id != current_user.id:
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
@login_required
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
@login_required
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
            login_user(user)
            session['user_id'] = user.id
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
@login_required
def logout():
    logout_user()
    flash("Signed out.", "info")
    return redirect(url_for('Home'))
#------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True,port=3000)

#------------------------------------------------------------------------------------------------
