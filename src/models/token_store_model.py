from src import db


class TokenStore(db.Model):
    access_token = db.Column(db.String(), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    refresh_token = db.Column(db.String())
    def __repr__(self):
        return '<User {}>'.format(self.email)