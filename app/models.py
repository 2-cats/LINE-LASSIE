# from datetime import datetime

# from flask_login import AnonymousUserMixin, UserMixin
# from werkzeug.security import check_password_hash, generate_password_hash

# from app import db

# from . import login_manager

# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key = True)
#     email = db.Column(db.String(64), unique=True, index=True)

#     def __repr__(self):
#         return '<User %r>' % self.username
