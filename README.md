# SweetShop - Confectionery Store

A complete Python/Flask web application for a local confectionery store with MySQL database integration. The application features user authentication, role-based access control, and product management.

## Features

- User registration and authentication
- Role-based access (User and Admin)
- Product catalog management (Admin only)
- Responsive web design
- MySQL database integration

## Technology Stack

- Backend: Python/Flask
- Database: MySQL
- ORM: Flask-SQLAlchemy
- Authentication: Flask-Login and Flask-Bcrypt
- Migrations: Flask-Migrate
- Forms: Flask-WTF
- Frontend: Bootstrap 5, Jinja2 templates

## Setup Instructions

### Prerequisites

- Python 3.7+
- MySQL Server

### Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy the `.env` file and update with your MySQL credentials:
     ```bash
     # .env
     FLASK_APP=run.py
     FLASK_ENV=development
     SECRET_KEY=your-secret-key-change-this-in-production
     SQLALCHEMY_DATABASE_URI=mysql+pymysql://username:password@localhost/sweetshop_db
     SQLALCHEMY_TRACK_MODIFICATIONS=False
     ```

5. **Initialize the database:**
   ```bash
   # Initialize migrations
   flask db init
   
   # Create migration
   flask db migrate -m "Initial migration"
   
   # Apply migration to create tables
   flask db upgrade
   ```

6. **Run the application:**
   ```bash
   flask run
   ```

7. **Access the application:**
   - Open your browser and navigate to `http://127.0.0.1:5000/`

### Creating an Admin User

To create an admin user, you can run the following commands in the Flask shell:

```bash
flask shell
```

Then in the shell:

```python
from app.models import User
from app.extensions import db

admin = User(username='admin', role='ADMIN')
admin.set_password('adminpassword')
db.session.add(admin)
db.session.commit()
```

### Usage

- **User Role**: Can view products and product details
- **Admin Role**: Can manage products (add, edit, delete) and access admin dashboard

## Project Structure

```
/sweetshop
|-- /app
|   |-- /auth                (Authentication Blueprint)
|   |   |-- __init__.py
|   |   |-- routes.py
|   |   |-- forms.py
|   |-- /admin               (Admin Blueprint)
|   |   |-- __init__.py
|   |   |-- routes.py
|   |   |-- forms.py
|   |-- /main                (Main/Public Blueprint)
|   |   |-- __init__.py
|   |   |-- routes.py
|   |-- /static
|   |   |-- /css
|   |   |   |-- style.css
|   |-- /templates
|   |   |-- /auth
|   |   |   |-- login.html
|   |   |   |-- register.html
|   |   |-- /admin
|   |   |   |-- dashboard.html
|   |   |   |-- manage_products.html
|   |   |   |-- _product_form.html
|   |   |-- /main
|   |   |   |-- home.html
|   |   |   |-- product_detail.html
|   |   |-- base.html        (Base template with navigation)
|   |-- __init__.py          (Application Factory)
|   |-- models.py            (SQLAlchemy Models)
|   |-- extensions.py        (Init extensions)
|   |-- decorators.py        (Custom decorators)
|-- /migrations              (Flask-Migrate folder)
|-- config.py                (Configuration classes)
|-- run.py                   (Entry point to run the app)
|-- requirements.txt
|-- .env
|-- README.md
```

## License

This project is created for educational purposes.