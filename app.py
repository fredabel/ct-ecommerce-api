from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Table, Column, String, Integer, Numeric, Date, DateTime, UniqueConstraint, select
from marshmallow import ValidationError
from typing import List
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# MySQL database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/ecommerce_api'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Creating our Base Model
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy and Marshmallow
db = SQLAlchemy(model_class=Base)
db.init_app(app)
ma = Marshmallow(app)

# Order Product Association Table
order_product = Table(
    "order_product",
    Base.metadata,
    Column("order_id", ForeignKey("orders.id")),
    Column("product_id", ForeignKey("products.id")),
    # Add a unique constraint to prevent duplicate entries
    UniqueConstraint("order_id", "product_id", name="uq_order_product")
)

# User Table
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(200))
    email: Mapped[str] = mapped_column(String(200),unique=True)
    
    # One-to-Many relationship with Order
    orders: Mapped[List["Order"]] = relationship("Order", back_populates="user")

#Order Table   
class Order(Base):
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[datetime] = mapped_column(DateTime)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    products: Mapped[List["Product"]] = relationship(secondary=order_product, back_populates="orders")
    user: Mapped["User"] = relationship("User", back_populates="orders")
    
#Product Table
class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    
    orders: Mapped[List["Order"]] = relationship(secondary=order_product, back_populates="products")

#======= Schema ========
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        include_fk = True  # Include foreign keys in the schema
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product    
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


#========== Routes =================

#Users
@app.route('/users',methods=['POST'])
def create_user():
    try:
        user_data = user_schema.load(request.json)
        # Check if the email already exists in the database
        user_exist = db.session.execute(select(User).where(User.email == user_data['email'])).scalar_one_or_none()
        if user_exist:
            return jsonify({"message": "A user with this email already exists"}), 400
        
        new_user = User(name=user_data['name'], email=user_data['email'], address=user_data['address'])
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201
    
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    

@app.route('/users', methods=['GET'])
def get_users():
    query = select(User)
    users = db.session.execute(query).scalars().all()
    return users_schema.jsonify(users), 200
    
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "User does not exist"}), 400
    return user_schema.jsonify(user), 200

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    try:
        user_data = user_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
   
    if user_data['email'] != user.email:
        # Check if the new email already exists in the database
        user_exist = db.session.execute(select(User).where(User.email == user_data['email'])).scalar_one_or_none()
        if user_exist:
            return jsonify({"message": "A user with this email already exists"}), 400
    
    user.name = user_data['name']
    user.email = user_data['email']
    user.address = user_data['address']
    
    db.session.commit()
    return user_schema.jsonify(user),200
@app.route('/users/<int:id>',methods=['DELETE'])
def delete_user(id):
    user = db.session.get(User, id)
    if not user:
        return jsonify({"message": "Invalid user id"}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted user {id}"})

#Products Route
@app.route('/products', methods=['POST'])
def create_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_product = Product(product_name=product_data['product_name'], price=product_data['price'])
    db.session.add(new_product)
    db.session.commit()
    
    return product_schema.jsonify(new_product), 201

@app.route('/products', methods=['GET'])
def get_products():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products_schema.jsonify(products), 200

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = db.session.get(Product, id)
    if not product:
        return jsonify({"message": "Product does not exist"}),400
    return product_schema.jsonify(product), 200

@app.route('/products/<int:id>',methods=['PUT'])
def update_product(id):
    product = db.session.get(Product,id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    product.product_name = product_data['product_name']
    product.price = product_data['price']
   
    db.session.commit()
    return product_schema.jsonify(product),200

@app.route('/products/<int:id>',methods=['DELETE'])
def delete_product(id):
    product = db.session.get(Product,id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Successfully deleted product {id}"})

# Orders Route
@app.route('/orders', methods=['POST'])
def create_order():
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_order = Order(
        order_date=order_data['order_date'],
        user_id=order_data['user_id']
    )
    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order), 201

#Add a product to an order (prevent duplicates)
@app.route('/orders/<int:order_id>/add_product/<int:product_id>', methods=['PUT'])
def add_product_to_order(order_id, product_id):
    # Fetch the order and product from the database
    order = db.session.get(Order, order_id)
    product = db.session.get(Product, product_id)

    # Check if the order and product exist
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    if not product:
        return jsonify({"message": "Invalid product id"}), 400

    # Check if the product is already in the order
    if product in order.products:
        return jsonify({"message": "Product already exists in the order"}), 400

    # Add the product to the order
    order.products.append(product)
    db.session.commit()

    return jsonify({"message": f"Product {product_id} added to order {order_id}"}), 200

#Get all orders for a user
@app.route('/orders/user/<int:user_id>',methods=['GET'])
def get_orders_per_user(user_id):
    user = db.session.get(User,user_id)
    if not user:
        return jsonify({"message": "Invalid order id"}), 400
    return  orders_schema.jsonify(user.orders), 200

#Get all products for an order
@app.route('/orders/<int:order_id>/products',methods=['GET'])
def get_all_products_from_order(order_id):
    order = db.session.get(Order,order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    return products_schema.jsonify(order.products),200

#Remove a a single product from an order
@app.route('/orders/<int:order_id>/remove_product/<int:product_id>', methods=['DELETE'])
def delete_product_from_order(order_id, product_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Invalid product id"}), 400
    # Check if the product is in the order
    if product not in order.products:
        return jsonify({"message": "Product not found in the order"}), 400
    order.products.remove(product)
    db.session.commit()
    
    return jsonify({"message": f"Product {product_id} removed from order {order_id}"}), 200
#Remove products from an order
@app.route('/orders/<int:order_id>/remove_product', methods=['DELETE'])
def delete_products_from_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({"message": "Invalid order id"}), 400
    
    # Get the list of product IDs from the request
    product_ids = request.json.get("product_ids", []) #[1,2,3]
    if not product_ids:
        return jsonify({"message": "No product IDs provided"}), 400
    
    # Iteratethe product IDs and remove them from the order
    removed_products = []
    for product_id in product_ids:
        product = db.session.get(Product, product_id)
        if not product:
            continue  # Skip invalid product IDs
        if product in order.products:
            order.products.remove(product)
            removed_products.append(product_id)
            
    # Commit the changes to the database
    db.session.commit()
    
    # Return a response with the list of removed product IDs
    return jsonify({
        "message": f"Products removed from order {order_id}",
        "removed_product_ids": removed_products
    }), 200
    

if __name__ == "__main__":
    
    with app.app_context():
        # db.drop_all()
        # db.create_all()
        pass
        
    app.run(debug=True)

