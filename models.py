from flask_login import UserMixin

from secret_santa import db


class User(db.Model, UserMixin):
    # __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.relationship(
        "Address",
        # backref="user",
        backref=db.backref("user", lazy=True),
        lazy=True,
        uselist=False,
    )

    def __repr__(self):
        return f"<User {self.name}>"


class Group(db.Model):
    # __bind_key__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer)
    is_raffled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Group {self.name}>"


class Member(db.Model):
    # __bind_key__ = 'members'
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    is_owner = db.Column(db.Boolean)

    def __repr__(self):
        return f"User.id <{self.user_id}> is member of group.id <{self.group_id}>"


class Santa(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer)
    presentee_id = db.Column(db.Integer)
    santa_id = db.Column(db.Integer)

    def __repr__(self):
        return f"Santa.id <{self.santa_id}> => User.id <{self.presentee_id}>, are member of group.id <{self.group_id}>"


class Address(db.Model):
    # __bind_key__ = 'address'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    description = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return f"<Address {self.description}>"
