**Prime Supplements** is a full-stack e-commerce web application built with Flask using the **Blueprint design pattern** to ensure modular, scalable, and organized code structure. The platform allows users to browse health supplements, manage a shopping cart, register/login securely, and write reviews.

## 🧠 Features

- 🛒 Product browsing, searching, filtering by category
- 🧾 Shopping cart system (session-based for guests, user-based for logged-in users)
- 🔐 User registration, login, and session management using Flask-Login and bcrypt
- 🗣️ Authenticated users can add, edit, and delete their own product reviews
- 💬 Flash messaging for feedback on user actions
- 📦 Product data creation with category-based organization
- 📁 Modular architecture using Flask Blueprints

## 💡 Technologies Used

### Backend
- Python
- Flask
- Flask Blueprints (modular structure)
- Flask-Login
- Flask-Bcrypt
- Flask-WTF / WTForms
- Flask-SQLAlchemy
- SQLite (local development database)

### Frontend
- HTML
- CSS
- Bootstrap

### Deployment
- Docker
- Docker Hub


## 🧪 Testing

This repository includes unit, integration, and UI (end-to-end) tests. The tests are organised under `tests/` and are designed to run locally and in CI.

### Test types and locations

- **Unit tests**: `tests/unit/` — test isolated functions and services (business logic, helpers).
- **Integration tests**: `tests/integration/` — exercise Flask routes, DB interactions, and combined components.
- **UI / E2E tests**: `tests/e2e/` (or `tests/ui/`) — browser-driven flows using Selenium (the project contains WebDriver-based tests).

### Running tests locally

Run the full test suite:

```bash
pytest
```

Run unit-only:

```bash
pytest tests/unit
```

Run coverage and generate a report:

```bash
coverage run --branch -m pytest
coverage report -m
```

Generate an HTML coverage report:

```bash
coverage run --branch -m pytest && coverage html
# open htmlcov/index.html
```

### Running UI (Selenium) tests

This project uses `webdriver-manager` to simplify WebDriver installation. To run UI tests headless (recommended for CI):

```bash
# example: run the e2e tests with headless chrome via environment variable (tests may read this)
pytest tests/e2e -k "not slow" -q
```

If your tests require a visible browser, omit headless configuration or set your WebDriver accordingly.

### Useful pytest flags

- `-k <expr>`: run subset matching an expression
- `-m <marker>`: run tests marked with a pytest marker
- `-q` / `-vv`: quiet or verbose
- `-n auto` (with `pytest-xdist`): run tests in parallel

### Test reporting & automation dashboard

The repository contains a small test dashboard app for viewing saved test results and screenshots (if present):

```bash
python test_dashboard/app.py
```

Open the dashboard at `http://localhost:5001`.

CI systems can also export `pytest-json-report` or `pytest-html` reports; this repo includes helpers to generate those formats.

## 🚀 Getting Started

1. **Clone the repository**  
```bash
git clone https://github.com/Mohamed-Abdelhakeem-x/Supplements-Store.git
cd Supplements-Store
```

2. **Install dependencies**  
```bash
pip install -r requirements.txt
```

3. **Run the app**  
```bash
flask run
```

4. **Or run via Docker**  
```bash
docker pull mohamedabdelhakeem/prime-supplements
docker run -p 3000:3000 mohamedabdelhakeem/prime-supplements
```

## 📂 Project Structure

```
Prime_Supplements/
│
├── Main/           # Home, About, and Shop routes
├── users/          # Registration, login, logout
├── cart/           # Cart logic and cart pages
├── Review/         # User review system
├── models.py       # SQLAlchemy models
├── forms/          # WTForms for auth, cart, and reviews
├── templates/      # HTML pages
├── static/         # CSS, JS, Images
│
tests/
│
├── unit/           # Unit tests: isolated service and helper logic (tests/unit)
├── integration/    # Integration tests: Flask routes, DB interactions (tests/integration)
├── ui/             # UI tests: older UI-focused tests (Selenium based, if used)
├── e2e/            # End-to-end tests: full browser flows and user scenarios (tests/e2e)
│
test_dashboard/    # Small Flask app that visualizes test reports and screenshots
│
├── templates/      # Dashboard HTML templates used by the app
│
```

## 📸 Screenshots
![Login Page](Screenshots/LoginPage.png)
![Shopping Page](Screenshots/ShoppingPage.png)
![Cart Page](Screenshots/CartPage.png)

## 🔗 Links

- 🐙 GitHub: [Supplements-Store](https://github.com/Mohamed-Abdelhakeem-x/Supplements-Store)
- 🐳 Docker Hub: [`mohamedabdelhakeem/prime-supplements`](https://hub.docker.com/r/mohamedabdelhakeem/prime-supplements)
- 🐳 run it by pulling the project then writing: docker run -p 3000:3000 mohamedabdelhakeem/prime-supplements:latest

## 👨‍💻 Author

**Mohamed Abdelhakeem**  
An aspiring Software Engineer passionate about building modern, scalable applications.

## 📝 License

This project is licensed under the [MIT License](LICENSE).
---

**Feel free to contribute and enhance the project! 🚀**
