from flask import Blueprint

cart = Blueprint("cart", __name__)

from Prime_Supplements.cart import routes