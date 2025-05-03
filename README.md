# Prime Supplements 🏋️‍♂️🧴

**Prime Supplements** is a full-stack Flask-based e-commerce web application for browsing, reviewing, and purchasing nutritional supplements.  
This project includes features like product search and filtering, shopping cart management, user authentication, product reviews, and more.

---

## 🚀 Features

- User registration, login, and logout
- Product browsing, search, and filtering by category
- Individual product pages with related item suggestions
- Shopping cart functionality (session-based or user-based)
- Product reviews (CRUD operations)
- Admin product seeding
- Responsive UI with Bootstrap

---

## 🛠️ Tech Stack

### Backend
- Python 3.11
- Flask
- Flask-WTF
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Login

### Frontend
- HTML5
- CSS3
- Bootstrap 5

---

## 🐳 Docker

You can run the app using Docker:

```bash
docker pull mohamedabdelhakeem/prime-supplements
docker run -p 3000:3000 mohamedabdelhakeem/prime-supplements
```

---

## 📂 Project Structure (Simplified)

```
Prime_Supplements/
├── Main/
├── cart/
├── users/
├── Review/
├── templates/
├── static/
│   └── css/
├── models.py
├── __init__.py
```

---

## 🧪 Initialize Database

On first run, the app seeds a list of sample products into the database.

---

## 🔗 Links

- **Docker Hub**: [`mohamedabdelhakeem/prime-supplements`](https://hub.docker.com/r/mohamedabdelhakeem/prime-supplements)
- **GitHub Repo**: [Supplements Store](https://github.com/Mohamed-Abdelhakeem-x/Supplements-Store)

---

## 📃 License

MIT License. Feel free to use and modify!

