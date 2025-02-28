# Supplements-Store

## Overview
Supplement Store is a web application built using Python, Flask, HTML, CSS, JavaScript, and Bootstrap. It allows users to browse and purchase dietary supplements conveniently online.

## Features
- User authentication (registration & login)
- Product catalog with categories
- Shopping cart functionality
- Secure checkout process
- Admin panel for managing products
- Responsive design using Bootstrap

## Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite/MySQL (choose based on setup)
- **Other:** Flask-WTF for forms, Flask-Login for authentication

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Mohamed-Abdelhakeem-x/Supplements-Store.git
   cd supplement-store
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```
5. Run the application:
   ```bash
   flask run
   ```
6. Open your browser and visit: `http://127.0.0.1:5000`

## Project Structure
```
project_root/
│-- app/
│   │-- static/
│   │-- templates/
│   │-- routes.py
│   │-- models.py
│   │-- forms.py
│-- migrations/
│-- venv/
│-- config.py
│-- requirements.txt
│-- run.py
```

## License
This project is licensed under the MIT License.