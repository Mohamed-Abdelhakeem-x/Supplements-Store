# Prime Supplements – Full Stack Flask Web App

A fully functional, blueprint-based Flask web application for an online supplements store. Users can browse products, register, log in, write reviews, and manage a shopping cart. The site is styled with Bootstrap and supports authentication, product management, and more.

---

## 🔧 Tech Stack

### Backend
- **Python 3**
- **Flask** – Web framework
- **Flask-WTF** – Secure form handling with CSRF protection
- **WTForms** – Form rendering and validation
- **Flask-SQLAlchemy** – ORM for database access
- **Flask-Bcrypt** – Password hashing
- **Flask-Login** – User authentication and session management
- **email-validator** – Validates emails during registration

### Frontend
- **HTML5**
- **CSS3**
- **Bootstrap 5** – UI styling and responsiveness

---

## 📦 Features

- 🔐 **User Authentication** (Register, Login, Logout)
- 🛍️ **Product Catalog** with images and descriptions
- 🛒 **Cart System** (session and user-based)
- ✍️ **User Reviews** (Add/Edit/Delete)
- 🧾 **Admin Product Initialization**
- 🧹 **Clear Cart Functionality**
- ✅ **Form Validation and Flash Messaging**

---

## 📂 Project Structure (Blueprint-Based)
## 🖥️ Pages and Functionalities

- `/` or `/Home`: Home page
- `/About`: About the store
- `/Shop`: Product listing with “Add to Cart” functionality
- `/Cart`: User cart summary and total price
- `/Reviews`: Authenticated user reviews
- `/register`: User registration
- `/login`: User login
- `/logout`: User logout
- `/clear_cart`: Clear current user's cart (POST)

## 📥 Installation Guide

### 1. Clone the Repository
git clone https://github.com/yourusername/supplements-store.git](https://github.com/Mohamed-Abdelhakeem-x/Supplements-Store

### 2. Clone the Repository
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

## 📥 Dependencies (requirements.txt)
Flask
Flask-WTF
WTForms
Flask-SQLAlchemy
Flask-Bcrypt
Flask-Login
email-validator

## 🚀 Live Deployment

Docker Hub Image: [mohamedabdelhakeem/supplements-store](https://hub.docker.com/r/mohamedabdelhakeem/prime-supplements)  
To run with Docker:
```bash
docker pull mohamedabdelhakeem/supplements-store
docker run -p 3000:3000 mohamedabdelhakeem/supplements-store
