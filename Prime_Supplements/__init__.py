from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '123 456 789'
import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Use in-memory database if in test mode, otherwise use MySQL database
if os.environ.get('TESTING_MODE'):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # Use DATABASE_URI from environment variables if running in Docker, else fallback to local connection
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URI', 
        'sqlite:///' + os.path.join(app.root_path, '..', 'instance', 'Orders.db')
    )

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def init_db():
    from Prime_Supplements.models import Product
    with app.app_context():
        db.create_all()
        
        if Product.query.count() == 0:
            products = [
                # Original Products
                Product(name="Gut Health+", description="Improve Digestion", price=44.99, image_url="/static/images/GutHealth+.png", category="Digestive Health"),
                Product(name="B Complex", description="Essential B Vitamins", price=44.99, image_url="/static/images/B-Complex.png", category="Vitamins"),
                Product(name="Fiber", description="Promote Digestive Health", price=44.99, image_url="/static/images/Fiber.png", category="Digestive Health"),
                Product(name="Liver", description="Support Optimal Liver Health", price=44.99, image_url="/static/images/Liver.png", category="Organ Support"),
                Product(name="Multi Mineral", description="Support Healthy Bones and Joints", price=44.99, image_url="/static/images/MultiMineral.png", category="Minerals"),
                Product(name="Multi Vitamin", description="Provide Essential Micronutrients", price=44.99, image_url="/static/images/MultiVitamin.png", category="Vitamins"),
                Product(name="Thyroid Support", description="Keep Thyroid Operating at Optimal Rate", price=44.99, image_url="/static/images/ThyroidSupport.png", category="Organ Support"),
                Product(name="Omega 3", description="Support Cardiovascular Health", price=44.99, image_url="/static/images/Omega3.png", category="Heart Health"),
                # New Products
                Product(name="Zinc Picolinate", description="Highly Bioavailable Zinc for Immune Support", price=19.99, image_url="/static/images/MultiMineral.png", category="Minerals"),
                Product(name="Magnesium Glycinate", description="Relaxation and Muscle Recovery", price=24.99, image_url="/static/images/MultiMineral.png", category="Minerals"),
                Product(name="Vitamin D3+K2", description="Bone Health and Immune Support", price=29.99, image_url="/static/images/MultiVitamin.png", category="Vitamins"),
                Product(name="Whey Protein Isolate", description="Fast Absorbing Protein for Muscle Growth", price=59.99, image_url="/static/images/GutHealth+.png", category="Protein"),
            ]
            db.session.add_all(products)
            db.session.commit()

# Only initialize production DB if not running tests
# Tests will configure their own databases
import sys
if not os.environ.get('TESTING_MODE'):
    init_db()
else:
    # In test mode - skip init_db() to protect Orders.db
    pass


from Prime_Supplements.Main.routes import main
from Prime_Supplements.users.routes import users
from Prime_Supplements.Review.routes import Reviews 
from Prime_Supplements.cart.routes import cart

app.register_blueprint(main)
app.register_blueprint(users)
app.register_blueprint(Reviews)
app.register_blueprint(cart)

# Delay user loader to break circular dependency
def set_user_loader():
    from Prime_Supplements.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

set_user_loader()