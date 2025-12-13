###Testing Whole Project
python -m pytest

###Testing a folder
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/ui/

###Testing Single Function
python -m pytest tests/unit/test_services.py::TestServiceLayer::test_user_authentication_logic

###Running the Dashboard
python -m pytest tests/ui/

###Running the Project
flask run