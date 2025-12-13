import unittest
from unittest.mock import MagicMock, patch
from Prime_Supplements.models import User, Product, Cart, CartItem, Review

class TestServiceLayer(unittest.TestCase):
    """
    Unit tests for the Service Layer logic (Models).
    Mocks database calls and external dependencies to ensure fault isolation.
    """

    def setUp(self):
        # Setup common mocks
        self.mock_db = MagicMock()

    @patch('Prime_Supplements.bcrypt')
    def test_user_authentication_logic(self, mock_bcrypt):
        """
        Test User authentication logic (check_password).
        Supports fault isolation by mocking bcrypt, isolating the User model logic.
        """
        # Arrange
        user = User(password="hashed_secret")
        mock_bcrypt.check_password_hash.return_value = True

        # Act
        result = user.check_password("secret")

        # Assert
        self.assertTrue(result)
        mock_bcrypt.check_password_hash.assert_called_with("hashed_secret", "secret")

    def test_product_availability_validation(self):
        """
        Test Product availability logic.
        Ensures product stock logic is correct without hitting the DB.
        """
        # Arrange
        product = Product(name="Test Vitamin", price=20.0)
        
        # Act
        is_available = product.get_stock_status()

        # Assert
        self.assertTrue(is_available)

    def test_cart_total_calculation(self):
        """
        Test Cart total calculation.
        Verifies the summing logic works correctly with multiple items.
        """
        # Arrange
        cart = Cart()
        product1 = Product(price=10.0)
        product2 = Product(price=20.0)
        
        item1 = CartItem(product=product1, quantity=2) # 20.0
        item2 = CartItem(product=product2, quantity=1) # 20.0
        
        # Mocking the relationship since we aren't using a real DB session
        cart.items = [item1, item2]

        # Act
        total = cart.calculate_total()

        # Assert
        self.assertEqual(total, 40.0)

    def test_cart_is_empty(self):
        """
        Test Cart is_empty check.
        """
        # Arrange
        cart = Cart()
        cart.items = []

        # Act & Assert
        self.assertTrue(cart.is_empty())
        
        # Arrange with item
        cart.items = [CartItem()]
        self.assertFalse(cart.is_empty())

    def test_review_validation_logic_valid(self):
        """
        Test Review content validation (Valid case).
        """
        # Arrange
        review = Review(title="Good", content="This is a great product!")

        # Act
        is_valid = review.validate_content()

        # Assert
        self.assertTrue(is_valid)

    def test_review_validation_logic_invalid_short(self):
        """
        Test Review content validation (Invalid: too short).
        """
        # Arrange
        review = Review(title="Bad", content="Hi")

        # Act
        is_valid = review.validate_content()

        # Assert
        self.assertFalse(is_valid)

    def test_review_validation_logic_invalid_long(self):
        """
        Test Review content validation (Invalid: too long).
        """
        # Arrange
        long_content = "a" * 501
        review = Review(title="Long", content=long_content)

        # Act
        is_valid = review.validate_content()

        # Assert
        self.assertFalse(is_valid)

if __name__ == '__main__':
    unittest.main()
