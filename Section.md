###Running the Dashboard
python test_dashboard/app.py

###Running the Project
flask run

###Testing Whole Project
python -m pytest
pytest tests/e2e -v

###Testing a folder
python -m pytest tests/unit/
python -m pytest tests/integration/
python -m pytest tests/ui/

###Testing Single Function
python -m pytest tests/unit/test_services.py::TestServiceLayer::test_user_authentication_logic