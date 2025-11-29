from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# --- App Setup ---
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Mina0630@localhost/ecommerce'

db = SQLAlchemy(app)
ma = Marshmallow(app)

# --- Models ---
order_items = db.Table(
    'order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False, default=1)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')
    products = db.relationship(
        'Product',
        secondary=order_items,
        lazy='subquery',
        backref=db.backref('orders', lazy=True)
    )

# --- Schemas ---
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

class OrderSchema(ma.SQLAlchemyAutoSchema):
    products = ma.Nested(ProductSchema, many=True)
    class Meta:
        model = Order
        load_instance = True
        include_fk = True

class UserSchema(ma.SQLAlchemyAutoSchema):
    orders = ma.Nested(OrderSchema, many=True)
    class Meta:
        model = User
        load_instance = True

user_schema = UserSchema()
users_schema = UserSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# --- DB Init ---
with app.app_context():
    db.create_all()

# --- CRUD Routes for User ---
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return user_schema.jsonify(new_user), 201

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    return users_schema.jsonify(all_users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return user_schema.jsonify(user)

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

# --- CRUD Routes for Product ---
@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@app.route('/products', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    return products_schema.jsonify(all_products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.get_json()
    product = Product.query.get_or_404(id)
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return jsonify({"message": "Product updated", "id": id}), 200

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'})

# --- CRUD Routes for Order ---
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    user_id = data['user_id']
    product_items = data.get('items', [])  # items: [{ "product_id": 1, "quantity": 2 }, ...]

    order = Order(user_id=user_id, status='pending')
    db.session.add(order)
    db.session.flush()  # get order.id before adding items

    for item in product_items:
        product = Product.query.get(item['product_id'])
        if product is None:
            continue  # or raise error
        quantity = item.get('quantity', 1)
        db.session.execute(
            order_items.insert().values(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity
            )
        )

    db.session.commit()
    return order_schema.jsonify(order), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    all_orders = Order.query.all()
    return orders_schema.jsonify(all_orders)

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order), 200

@app.route('/orders/<int:id>', methods=['PUT', 'PATCH'])
def update_order(id):
    data = request.get_json()
    order = Order.query.get_or_404(id)
    order.status = data.get('status', order.status)
    # You can add logic to update items if needed
    db.session.commit()
    return jsonify({"message": "Order updated", "id": id}), 200

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully", "order_id": order_id}), 200

# --- Home Route ---
@app.route('/')
def home():
    return "E-Commerce API is running!"

#Collection for all endpoints in the Flask Ecommerce API project:
#Users, Products, Orders, Auth (if any).

if __name__ == '__main__':
    app.run(debug=True)


