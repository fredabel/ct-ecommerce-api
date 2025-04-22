# E-Commerce API

This project is a RESTful API for managing an e-commerce platform. It allows users to manage **users**, **products**, and **orders**. The API is built using **Flask**, **SQLAlchemy**, and **Marshmallow** for database modeling, serialization, and validation.

---

## Features

### Users
- **Create a User**: Add a new user to the database with hashed passwords.
- **Get All Users**: Retrieve a list of all users (passwords are excluded from the response).
- **Get a User by ID**: Retrieve details of a specific user.
- **Update a User**: Update user details (e.g., name, email, address).
- **Delete a User**: Remove a user from the database.
- **Login**: Authenticate a user and generate a JWT token.

### Products
- **Create a Product**: Add a new product to the database.
- **Get All Products**: Retrieve a list of all products.
- **Get a Product by ID**: Retrieve details of a specific product.
- **Update a Product**: Update product details (e.g., name, price).
- **Delete a Product**: Remove a product from the database.

### Orders
- **Create an Order**: Add a new order for a user.
- **Add a Product to an Order**: Add a product to an existing order (prevents duplicates).
- **Get All Orders for a User**: Retrieve all orders placed by a specific user.
- **Get All Products in an Order**: Retrieve all products associated with a specific order.
- **Remove a Product from an Order**: Remove a single product from an order.
- **Remove Multiple Products from an Order**: Remove multiple products from an order.

---

## Technologies Used

- **Flask**: Web framework for building the API.
- **SQLAlchemy**: ORM for database modeling and querying.
- **Marshmallow**: For serialization and validation.
- **MySQL**: Database for storing users, products, and orders.
- **Flask-Bcrypt**: For hashing and verifying passwords.
- **Flask-JWT-Extended**: For authentication using JSON Web Tokens (JWT).
- **Flask-Migrate**: For database migrations.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/ecommerce-api.git
   cd ecommerce-api
2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install dependencies**:
   ```bash
    pip install -r requirements.txt
4. **Set Up the Database**:
   ```bash
   CREATE DATABASE ecommerce_api;
5. **Create the .env file with your credentials**:
   ```bash
   DATABASE_URL=mysql+mysqlconnector://username:password@localhost/ecommerce_api
   JWT_SECRET_KEY=your_secret_key
6. **Run Database Migrations**:
   ```bash
   flask db upgrade
7. **Run Application**:
   ```bash
   python app.py
8. **Access API**:
   ```bash
   Access the API: The API will be available at http://127.0.0.1:5000