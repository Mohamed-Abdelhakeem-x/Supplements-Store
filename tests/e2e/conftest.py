import pytest
import threading
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from Prime_Supplements import app, db, bcrypt
from Prime_Supplements.models import User, Product, CartItem, Cart

# --- Server Fixtures ---

@pytest.fixture(scope='session')
def app_port():
    """Returns a free port for the Flask server."""
    return 5005

@pytest.fixture(scope='session')
def live_server_url(app_port):
    """Returns the root URL of the live server."""
    return f'http://localhost:{app_port}'



@pytest.fixture(scope='session', autouse=True)
def run_app_server(app_port):
    """Runs the Flask app in a background thread."""
    # Use a unique DB for each session to avoid file locking issues
    import uuid
    import shutil
    
    unique_id = str(uuid.uuid4())[:8]
    db_filename = f'test_e2e_{unique_id}.db'
    db_path = os.path.join(os.getcwd(), 'instance', db_filename)
    
    # Configure App
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'test_secret_e2e_suite'
    
    # Ensure clean DB start
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            pass # Best effort

    # Initialize DB and Seed Data
    with app.app_context():
        # Dispose old engine if it exists to release locks
        try:
            db.engine.dispose()
        except:
            pass
            
        db.create_all()
        seed_test_data()

    def start_server():
        # use_reloader=False is important for threading
        # threaded=True is default
        app.run(port=app_port, use_reloader=False, threaded=True)

    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()
    
    # Give server time to start
    time.sleep(3) 
    
    yield
    
    # Teardown
    with app.app_context():
        db.session.remove()
        try:
            db.engine.dispose()
        except:
            pass

    # Give some time for file handles to close
    time.sleep(1)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError:
            print(f"Warning: Could not delete test DB {db_path} - likely file lock.")

def seed_test_data():
    """Seeds the database with initial data for testing."""
    # Clear existing data to prevent IntegrityErrors if DB wasn't clean
    try:
        db.session.query(User).delete()
        db.session.query(Product).delete()
        db.session.commit()
    except:
        db.session.rollback()

    # Create a test user
    hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
    user = User(username="e2euser", email="e2e@example.com", phone="1112223333", password=hashed_pw)
    
    # Create test products
    p1 = Product(name="E2E Whey Protein", price=50.0, category="Protein", description="Test Protein", image_url="/static/images/p1.png")
    p2 = Product(name="E2E Vitamin C", price=15.0, category="Vitamins", description="Health boost", image_url="/static/images/p2.png")
    
    db.session.add(user)
    db.session.add(p1)
    db.session.add(p2)
    db.session.commit()

# --- WebDriver Fixtures ---

@pytest.fixture(scope='function')
def driver():
    """set up chrome driver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # chrome_options.add_argument("--disable-gpu") 

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(5) # Set a default implicit wait
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope='function')
def authorized_driver(driver, live_server_url):
    """Returns a driver instance that is already logged in."""
    driver.get(f"{live_server_url}/login")
    from selenium.webdriver.common.by import By
    
    driver.find_element(By.NAME, "email").send_keys("e2e@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.ID, "login").click() # ID derived from inspection
    
    return driver
