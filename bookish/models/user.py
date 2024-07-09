from bookish.app import db


class User(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'User'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    password = db.Column(db.String())
    token = db.Column(db.String())

    def __init__(self, name, password, token):
        self.name = name
        self.password = password
        self.token = token

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            'token': self.token
        }
