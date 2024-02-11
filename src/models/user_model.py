from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)


    def __repr__(self):
        return '<User {}>'.format(self.email)