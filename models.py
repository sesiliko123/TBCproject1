from datetime import datetime, timezone
from ext import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# 👤 მომხმარებლის მოდელი
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    role = db.Column(db.String(20), default='User')
    profile_image = db.Column(db.String(100), nullable=True)

    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, username, password, first_name, last_name, gender, role='User', profile_image=None):
        self.username = username
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.role = role
        self.profile_image = profile_image or ('default_female.png' if gender == 'მდედრობითი' else 'default_male.png')

    @property
    def password(self):
        raise AttributeError("პაროლის ნახვა არ შეიძლება")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# 📦 პროდუქტის მოდელი
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))

    # საერთო ტექნიკური მონაცემები
    storage = db.Column(db.String(50))         # შიდა მეხსიერება
    ram = db.Column(db.String(50))             # ოპერატიული მეხსიერება
    screen_size = db.Column(db.String(50))     # ეკრანის ზომა
    resolution = db.Column(db.String(50))      # ეკრანის რეზოლუცია
    refresh_rate = db.Column(db.String(50))    # განახლების სიხშირე
    screen_type = db.Column(db.String(50))     # ეკრანის ტიპი
    bluetooth = db.Column(db.String(50))       # Bluetooth
    battery = db.Column(db.String(50))         # ელემენტი

    # ყურსასმენებისთვის
    noise_cancellation = db.Column(db.Boolean) # ხმის დახშობა (ANC)
    battery_life = db.Column(db.String(50))    # ელემენტის ხანგრძლივობა
    charging_time = db.Column(db.String(50))   # დამუხტვის დრო

    # სხვა ტექნიკური ველები
    type_c = db.Column(db.String(50))          # Type-C
    processor = db.Column(db.String(100))      # პროცესორის ტიპი
    cores = db.Column(db.String(50))           # ბირთვები
    frequency = db.Column(db.String(50))       # სიხშირე
    viewing_angle = db.Column(db.String(50))   # ხედვის კუთხე (მონიტორები)
    work_time = db.Column(db.String(50))       # სამუშაო დრო (საათები/კონსოლი)

    # ურთიერთობები
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviews = db.relationship('Review', back_populates='product', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='product', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
    user = db.relationship('User', backref='products')

# 🛒 კალათის ელემენტი
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    user = db.relationship('User', back_populates='cart_items')
    product = db.relationship('Product', back_populates='cart_items')


# ✍️ მიმოხილვა
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    product = db.relationship('Product', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')


# 🧾 შეკვეთა
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='დასრულებული')
    date_ordered = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
