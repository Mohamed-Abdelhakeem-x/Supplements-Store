from flask import Flask, render_template , redirect, url_for, flash, session
from forms import RegisterForm, LoginForm, CartForm
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = '123 456 789'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Orders.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    image_url = db.Column(db.String(300))

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100))

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, default=1)

    cart = db.relationship('Cart', backref=db.backref('items', lazy=True))
    product = db.relationship('Product')


with app.app_context():
     db.create_all()

@app.route('/')
@app.route("/Home", methods=['GET','POST'])
def Home():
    return render_template('Home.HTML', title = "Home", cssFile = "Static/css/Home.css")

@app.route("/About")
def about():
    return render_template('About.HTML', title = "About", cssFile = "Static/css/About.css")

@app.route("/Shop")
def Shop():
    products = Product.query.all()
    return render_template('Shop.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Create session id if not exist
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())

    session_id = session['session_id']

    # Get or create cart
    cart = Cart.query.filter_by(session_id=session_id).first()
    if not cart:
        cart = Cart(session_id=session_id)
        db.session.add(cart)
        db.session.commit()

    # Get or create cart item
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
    # Only create if no products exist
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
    if 'session_id' not in session:
        cart_items = []
        total = 0.0
    else:
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
        if cart:
            cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
            total = sum(item.product.price * item.quantity for item in cart_items)
        else:
            cart_items = []
            total = 0.0
    return render_template('Cart.Html', cart_items=cart_items, total=total)

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    if 'session_id' in session:
        session_id = session['session_id']
        cart = Cart.query.filter_by(session_id=session_id).first()
        if cart:
            # Delete all items in the user's cart
            CartItem.query.filter_by(cart_id=cart.id).delete()
            db.session.commit()
    return redirect(url_for('CartPage'))

@app.route('/login', methods=['GET','POST'])
def login():
   form = LoginForm()
   if form.validate_on_submit():
       if form.email.data == "mohamed.abdelhakeem@gmail.com" and form.password.data == "123456":
            flash("Logged in successfully!", "success")
            return redirect(url_for("Home"))
       else:
            flash("Invalid email or password.", "danger")
   return render_template('login.HTML', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
   form = RegisterForm()
   if form.validate_on_submit():
      flash(f"Account created for {form.username.data}!", "success")
      return redirect(url_for("login"))
   return render_template('signup.HTML',form=form)


if __name__ == "__main__":
    app.run(debug=True,port=3000)

