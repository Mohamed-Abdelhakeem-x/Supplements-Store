import pytest
from Prime_Supplements import app, db, bcrypt
from Prime_Supplements.models import User, Product, Cart, CartItem

@pytest.fixture
def client():
    # Configure app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for easier form testing
    app.config['SECRET_KEY'] = 'test_secret'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def init_database():
    # Create initial data for tests
    hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(username="testuser", email="test@example.com", phone="12345678901", password=hashed_pw)
    product = Product(name="Test Vitamin", price=20.0, category="Health", description="Test Desc")
    db.session.add(user)
    db.session.add(product)
    db.session.commit()
    return db
