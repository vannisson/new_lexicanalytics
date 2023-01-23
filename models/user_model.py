from database import db
import uuid
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=uuid.uuid4())
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    productions = db.relationship('Production', backref='users', lazy=True)