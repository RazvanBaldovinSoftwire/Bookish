from datetime import datetime

from sqlalchemy import ForeignKey

from bookish.app import db
from bookish.models.book import Book
from bookish.models.user import User


class Borrows(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Borrows'

    # Here we outline what columns we want in our database
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, ForeignKey(User.id))
    isbn = db.Column(db.String(), ForeignKey(Book.isbn))
    return_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, id_user, isbn, return_date):
        self.id_user = id_user
        self.isbn = isbn
        self.return_date = return_date

    def serialize(self):
        return {
            'Borrow ID': self.id,
            'User ID': self.id_user,
            'ISBN Book': self.isbn,
            'Return Date': self.return_date
        }
