from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mina0630@localhost/app_db'
db = SQLAlchemy(app)


# Define User model if not imported
class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    
class Product(db.Model):
    __tablename__ = 'Products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Order(db.Model):
    __tablename__ = 'Orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('Products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# Create tables in MySQL
with app.app_context():
    db.create_all()

def create_user_direct(name, email):
    with app.app_context():
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {user.id}, {user.name}, {user.email}")

@app.route('/users', methods=['POST'])



# Only run direct creation functions when executing the script directly

# Move this block to the end of the file

def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "Invalid input"}), 400
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

def test_create_user(client):
    response = client.post('/users', json={"name": "Alice", "email": "alice@example.com"})
    assert response.status_code == 201

# Direct creation function for Product
def create_product_direct(name, price):
    with app.app_context():
        product = Product(name=name, price=price)
        db.session.add(product)
        db.session.commit()
        print(f"Created product: {product.id}, {product.name}, {product.price}")

create_product_direct("Widget", 19.99)

# Direct creation function for Order
def create_order_direct(user_id, product_id, quantity):
    with app.app_context():
        order = Order(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(order)
        db.session.commit()
        print(f"Created order: {order.id}, user_id: {order.user_id}, product_id: {order.product_id}, quantity: {order.quantity}")

create_order_direct(1, 1, 2)

# Create a Flask route to handle POST requests to /orders
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    # Validate input
    if not data or 'user_id' not in data or 'product_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Check user existence
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Check product existence
    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({"error": "Product not found"}), 404

    # Create order
    order = Order(user_id=user.id, product_id=product.id, quantity=data['quantity'])
    db.session.add(order)
    db.session.commit()

    # Prepare summary
    summary = {
        "order_id": order.id,
        "user": user.name,
        "product": product.name,
        "quantity": order.quantity,
        "total_price": product.price * order.quantity
    }
    return jsonify(summary), 201
def hello():
    return "Hello, world!"