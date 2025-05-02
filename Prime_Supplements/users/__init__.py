from flask import Blueprint

users = Blueprint("users", __name__)

from Prime_Supplements.users import routes