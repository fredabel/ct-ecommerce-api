## 
# E-Commerce API

This project is a RESTful API for managing an e-commerce platform. It allows users to manage **users**, **products**, and **orders**. The API is built using **Flask**, **SQLAlchemy**, and **Marshmallow** for database modeling, serialization, and validation.

---

## Features

### Users
- **Create a User**: Add a new user to the database.
- **Get All Users**: Retrieve a paginated list of all users.
- **Get a User by ID**: Retrieve details of a specific user.
- **Update a User**: Update user details (e.g., name, email, address).
- **Delete a User**: Remove a user from the database.

### Products
- **Create a Product**: Add a new product to the database.
- **Get All Products**: Retrieve a paginated list of all products.
- **Get a Product by ID**: Retrieve details of a specific product.
- **Update a Product**: Update product details (e.g., name, price).
- **Delete a Product**: Remove a product from the database.

### Orders
- **Create an Order**: Add a new order for a user.
- **Add a Product to an Order**: Add a product to an existing order (prevent duplicates).
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

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/ecommerce-api.git
   cd ecommerce-api
2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt