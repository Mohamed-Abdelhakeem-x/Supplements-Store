import unittest
from unittest.mock import patch, MagicMock
from Prime_Supplements import init_db, db
from Prime_Supplements.models import Product, User

class TestInitApp(unittest.TestCase):
    def test_init_db_creates_data(self):
        """Test that init_db creates initial products if table is empty."""
        
        # We need to run this with an app context
        from Prime_Supplements import app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        
        with app.app_context():
            # Ensure clean state
            db.drop_all()
            db.create_all()
            
            # Verify empty
            assert Product.query.count() == 0
            
            # Call init_db
            init_db()
            
            # Verify Products created
            assert Product.query.count() > 0
            p = Product.query.filter_by(name="Gut Health+").first()
            assert p is not None

    def test_init_db_skips_if_exists(self):
        """Test that init_db does not duplicate data."""
        from Prime_Supplements import app
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        
        with app.app_context():
            db.drop_all()
            db.create_all()
            
            # Create one product manually
            p = Product(name="Existing", price=10)
            db.session.add(p)
            db.session.commit()
            
            # Call init_db
            init_db()
            
            # Logic says: if Product.query.first(): return
            # So duplicate products should NOT be added
            assert Product.query.count() == 1
            assert Product.query.first().name == "Existing"
