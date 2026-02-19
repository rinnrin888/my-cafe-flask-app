from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CafeItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))   # Coffee, Bakery, Tea
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(255))