from flask_login import UserMixin
from secret_santa import db

class Users(db.Model, UserMixin):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f"<User {self.name}>"


class Groups(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer)

    def __repr__(self):
        return f"<Group {self.name}>"


class Members(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    is_owner = db.Column(db.Boolean)

    def __repr__(self):
        return f"User.id <{self.user_id}> is member of group.id <{self.group_id}>"
