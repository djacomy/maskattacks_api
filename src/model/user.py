from flask_bcrypt import generate_password_hash, check_password_hash

from werkzeug.security import generate_password_hash, check_password_hash

from .abc import db, BaseModel


class User(db.Model, BaseModel):
    __tablename__ = 'auth_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))

    def __init__(self, email=None, password=None, username=None):
        if email:
            self.email = email.lower()
        if password:
            self.set_password(password)
        if username:
            self.username = username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def json(self):
        return {
            "id": self.id,
            "username": self.username
        }, 200

    # Method to save user to DB
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by username
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
