from . import db

class Users(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Groups(db.Model):
    # primary keys are required by SQLAlchemy
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True)
    owner_id = db.Column(db.Integer)


if __name__ == '__main__':
    db.create_all()
