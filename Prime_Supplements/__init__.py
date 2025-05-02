from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = '123 456 789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Orders.db'

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

init_db()


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
        return User.query.get(int(user_id))

set_user_loader()