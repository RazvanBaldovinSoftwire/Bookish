from bookish.app import db


class Book(db.Model):
    # This sets the name of the table in the database
    __tablename__ = 'Book'

    # Here we outline what columns we want in our database
    isbn = db.Column(db.String(), primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    copies = db.Column(db.Integer)
    available = db.Column(db.Integer)

    def __init__(self, isbn, title, author, copies,available):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.copies = copies
        self.available = available

    def __repr__(self):
        return '<isbn {}>'.format(self.isbn)

    def serialize(self):
        return {
            'ISBN': self.isbn,
            'Title': self.title,
            'Author': self.author,
            'Copies': self.copies,
            'Available': self.available,
        }
