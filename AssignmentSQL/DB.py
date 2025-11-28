from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('mysql+mysqlconnector://root:Mina0630@localhost:3306/db_py')
Base = declarative_base()

# Association object for many-to-many relationship with quantity
class OrderProduct(Base):
    __tablename__ = 'order_product'
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer, nullable=False, default=1)
    order = relationship("Order", back_populates="order_products")
    product = relationship("Product", back_populates="order_products")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String(20), nullable=False, default='not shipped')
    user = relationship('User', back_populates='orders')
    order_products = relationship('OrderProduct', back_populates='order')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    order_products = relationship('OrderProduct', back_populates='product')

Base.metadata.create_all(engine)
print("Tables created!")

Session = sessionmaker(bind=engine)
session = Session()

new_user1 = User(username="toddsmith", email="toddsmith@example.com")
new_user2 = User(username="markjones", email="markjones@example.com")
new_user3 = User(username="drea_wilson", email="drea_wilson@example.com")
session.add(new_user1)
session.add(new_user2)
session.add(new_user3)
session.commit()

print("User added:", new_user1.username)
print("User added:", new_user2.username)
print("User added:", new_user3.username)

Session = sessionmaker(bind=engine)
session = Session()

product1 = Product(name="Laptop", price=1200)
product2 = Product(name="Phone", price=800)
product3 = Product(name="Tablet", price=400)

session.add_all([product1, product2, product3])
session.commit()

print("Products added:", product1.name, product2.name, product3.name)

Session = sessionmaker(bind=engine)
session = Session()

user = session.query(User).filter_by(username="toddsmith").first()
product1 = session.query(Product).filter_by(name="Laptop").first()

user = session.query(User).filter_by(username="markjones").first()
product2 = session.query(Product).filter_by(name="Phone").first()

user = session.query(User).filter_by(username="drea_wilson").first()
product3 = session.query(Product).filter_by(name="Tablet").first()

order = Order(user=user, status='not shipped')
order_product1 = OrderProduct(product=product1, quantity=2)
order_product2 = OrderProduct(product=product2, quantity=1)
order.order_products = [order_product1, order_product2]
session.add(order)
session.commit()

print("Order added for user:", user.username)

Session = sessionmaker(bind=engine)
session = Session()

# Update all orders to shipped
orders = session.query(Order).all()
for order in orders:
    order.status = "shipped"
session.commit()

print("All orders updated to shipped.")

Session = sessionmaker(bind=engine)
session = Session()

print("Each user now has a product and an order.")

Session = sessionmaker(bind=engine)
session = Session()

users = session.query(User).all()
products = session.query(Product).all()

for user, product in zip(users, products):
    order = Order(user=user, status='not shipped')
    order_product = OrderProduct(product=product, quantity=1)
    order.order_products = [order_product]
    session.add(order)
session.commit()

print("Each user now has a product and an order.")

# Retrieve all users and print their information
users = session.query(User).all()
for user in users:
    print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")

# Retrieve all products and print their name and price
products = session.query(Product).all()
for product in products:
    print(f"Product ID: {product.id}, Name: {product.name}, Price: {product.price}")

# Retrieve all orders, showing the user’s name, product name, and quantity
orders = session.query(Order).all()
for order in orders:
    print(f"Order ID: {order.id}, User: {order.user.username if order.user else 'Deleted User'}, Status: {order.status}")
    for op in order.order_products:
        print(f"  Product: {op.product.name}, Quantity: {op.quantity}")

# Update a product’s price
product_to_update = session.query(Product).filter_by(name="Laptop").first()
if product_to_update:
    product_to_update.price = 1500
    session.commit()
    print(f"Updated price for {product_to_update.name}: {product_to_update.price}")

# Delete a user by ID
user_id_to_delete = 1  # Change this to the desired user ID
user_to_delete = session.get(User, user_id_to_delete)
if user_to_delete:
    session.delete(user_to_delete)
    session.commit()
    print(f"Deleted user with ID: {user_id_to_delete}")

# Query orders and show quantities, handle deleted users
orders = session.query(Order).all()
for order in orders:
    user_name = order.user.username if order.user else "Deleted User"
    print(f"Order ID: {order.id}, User: {user_name}, Status: {order.status}")
    for op in order.order_products:
        print(f"  Product: {op.product.name}, Quantity: {op.quantity}")